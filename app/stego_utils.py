print("STEGO UTILS LOADED")
import cv2
from app.crypto_utils import (
    blowfish_encrypt,
    decrypt_fake_DNA,
    encrypt_to_fake_DNA,
    dna_to_binary,
    binary_to_fake_DNA
)

# ---------------- EMBED BITS ----------------
def embed_data(frame, data):
    flat = frame.flatten()

    if len(data) > len(flat):
        raise ValueError("Message too large for this video frame")

    for i in range(len(data)):
        flat[i] = (flat[i] & 254) | int(data[i])

    return flat.reshape(frame.shape)


# ---------------- EXTRACT BITS ----------------
def extract_bits(frame, count):
    flat = frame.flatten()
    return ''.join(str(flat[i] & 1) for i in range(count))


# ---------------- ENCRYPT ----------------
def embedding(video_path, message, key):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Cannot open input video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'FFV1')

    out = cv2.VideoWriter(
        "app/static/stego_video.avi",
        fourcc,
        fps,
        (width, height)
    )

    if not out.isOpened():
        raise ValueError("VideoWriter failed to open")

    ret, frame = cap.read()
    if not ret:
        raise ValueError("Cannot read first frame")

    # 🔥 IMPORTANT FIX
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    encrypted = blowfish_encrypt(message, key)
    dna = encrypt_to_fake_DNA(encrypted)
    binary = dna_to_binary(dna)

    payload = format(len(binary), '032b') + binary

    frame = embed_data(frame, payload)
    out.write(frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    print("Encryption completed successfully")



# ---------------- DECRYPT ----------------
def extraction(video_path):

    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise ValueError("Cannot read stego frame")

    header = extract_bits(frame, 32)
    length = int(header, 2)

    print("HEADER:", header)
    print("LENGTH:", length)

    if length <= 0:
        raise ValueError("No hidden data found")

    binary = extract_bits(frame, 32 + length)[32:]
    dna = binary_to_fake_DNA(binary)

    return decrypt_fake_DNA(dna)
