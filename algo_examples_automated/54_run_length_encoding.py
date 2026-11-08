"""
Run-Length Encoding (RLE) — Compression and Decompression
=========================================================

Run-length encoding is a simple lossless compression algorithm that replaces
consecutive repeated values (runs) with a count and the value itself.

This module provides:
  - rle_compress:  Encode a byte sequence into RLE format.
  - rle_decompress: Decode an RLE byte sequence back to the original.
  - Text and binary examples in the __main__ block.

Format used:
  Each run is encoded as two bytes: [count, value].
  - count  : 1–255 (0 is reserved / not used for a run).
  - value  : the byte value being repeated.
  - A run longer than 255 is split into multiple segments.
  - A single non-repeated byte is stored as count=1.

This is a straightforward, educational implementation suitable for
learning and demonstration purposes.
"""

from typing import Union


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _to_bytes(data: Union[str, bytes]) -> bytes:
    """Convert str to UTF-8 bytes; pass bytes through unchanged."""
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError(f"Expected str or bytes, got {type(data).__name__}")


def _from_bytes(data: bytes, as_text: bool) -> Union[str, bytes]:
    """Decode bytes to str if as_text is True; otherwise return raw bytes."""
    if as_text:
        return data.decode("utf-8")
    return data


# ---------------------------------------------------------------------------
# Compression
# ---------------------------------------------------------------------------

def rle_compress(data: Union[str, bytes]) -> bytes:
    """Compress data using run-length encoding.

    Args:
        data: Input string or bytes to compress.

    Returns:
        RLE-encoded bytes.  Each pair of output bytes is (count, value),
        where count is in the range 1–255.

    Example:
        >>> rle_compress("AAABBBCC")
        b'\\x03A\\x03B\\x02C'
    """
    raw = _to_bytes(data)
    if not raw:
        return b""

    compressed: list[int] = []
    i = 0

    while i < len(raw):
        current_byte = raw[i]
        run_length = 1

        # Count consecutive identical bytes, up to 255.
        while i + run_length < len(raw) and raw[i + run_length] == current_byte:
            run_length += 1
            if run_length == 255:
                break

        compressed.append(run_length)
        compressed.append(current_byte)
        i += run_length

    return bytes(compressed)


# ---------------------------------------------------------------------------
# Decompression
# ---------------------------------------------------------------------------

def rle_decompress(compressed: bytes, as_text: bool = False) -> Union[str, bytes]:
    """Decompress RLE-encoded bytes back to the original data.

    Args:
        compressed: RLE-encoded byte sequence (pairs of [count, value]).
        as_text:    If True, decode the result as UTF-8 text; otherwise
                    return raw bytes.

    Returns:
        The decompressed string (if as_text=True) or bytes.

    Raises:
        ValueError: If compressed data has an odd length (malformed).

    Example:
        >>> rle_decompress(b'\\x03A\\x03B\\x02C')
        'AAABBBCC'
    """
    if len(compressed) % 2 != 0:
        raise ValueError(
            f"Compressed data must have even length (got {len(compressed)})"
        )

    decompressed: list[int] = []

    for i in range(0, len(compressed), 2):
        count = compressed[i]
        value = compressed[i + 1]

        if count == 0:
            raise ValueError(f"Invalid run length 0 at position {i}")

        decompressed.extend([value] * count)

    return _from_bytes(bytes(decompressed), as_text)


# ---------------------------------------------------------------------------
# Convenience wrappers for text
# ---------------------------------------------------------------------------

def compress_text(text: str) -> bytes:
    """Compress a text string with RLE.

    Args:
        text: The string to compress (encoded as UTF-8 internally).

    Returns:
        RLE-compressed bytes.
    """
    return rle_compress(text)


def decompress_to_text(compressed: bytes) -> str:
    """Decompress RLE bytes back to a text string.

    Args:
        compressed: RLE-compressed bytes.

    Returns:
        The original UTF-8 decoded string.
    """
    return rle_decompress(compressed, as_text=True)  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Pretty-printing helper
# ---------------------------------------------------------------------------

def format_rle(compressed: bytes) -> str:
    """Format RLE bytes as a human-readable list of (count, value) pairs.

    Args:
        compressed: RLE-encoded bytes.

    Returns:
        A string like "(3, 65) (3, 66) (2, 67)" for b'\\x03A\\x03B\\x02C'.
    """
    pairs = []
    for i in range(0, len(compressed), 2):
        count = compressed[i]
        value = compressed[i + 1]
        # Show printable ASCII chars repr() style; show hex for others.
        if 32 <= value <= 126:
            val_repr = f"'{chr(value)}'"
        else:
            val_repr = f"0x{value:02x}"
        pairs.append(f"({count}, {val_repr})")
    return " ".join(pairs)


# ---------------------------------------------------------------------------
# Example usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Run-Length Encoding — Examples")
    print("=" * 60)

    # ---- Text example 1: Simple repeated characters -----------------------
    text1 = "AAABBBCCCDDD"
    comp1 = compress_text(text1)
    decomp1 = decompress_to_text(comp1)

    print(f"\n--- Text Example 1: Simple repetition ---")
    print(f"  Original  : {text1!r}")
    print(f"  Compressed: {comp1!r}  ({len(comp1)} bytes)")
    print(f"  RLE pairs : {format_rle(comp1)}")
    print(f"  Decompressed: {decomp1!r}")
    print(f"  Round-trip OK: {text1 == decomp1}")

    # ---- Text example 2: Mixed content -----------------------------------
    text2 = "WWWWWWWWWWBBBWWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWW"
    comp2 = compress_text(text2)
    decomp2 = decompress_to_text(comp2)

    print(f"\n--- Text Example 2: Mixed runs ---")
    print(f"  Original  : {text2!r}  ({len(text2)} chars)")
    print(f"  Compressed: {comp2!r}  ({len(comp2)} bytes)")
    print(f"  RLE pairs : {format_rle(comp2)}")
    print(f"  Decompressed: {decomp2!r}")
    print(f"  Round-trip OK: {text2 == decomp2}")

    # ---- Text example 3: No repetition (worst case) ----------------------
    text3 = "ABCDEFGHIJ"
    comp3 = compress_text(text3)
    decomp3 = decompress_to_text(comp3)

    print(f"\n--- Text Example 3: No repetition (expansion) ---")
    print(f"  Original  : {text3!r}  ({len(text3)} chars)")
    print(f"  Compressed: {comp3!r}  ({len(comp3)} bytes)")
    print(f"  RLE pairs : {format_rle(comp3)}")
    print(f"  Decompressed: {decomp3!r}")
    print(f"  Round-trip OK: {text3 == decomp3}")
    print(f"  Note: Non-repeating data expands (2 bytes per input byte).")

    # ---- Text example 4: Long run (>255) ---------------------------------
    text4 = "X" * 300 + "Y" * 100
    comp4 = compress_text(text4)
    decomp4 = decompress_to_text(comp4)

    print(f"\n--- Text Example 4: Long runs (>255) ---")
    print(f"  Original  : 300 X's + 100 Y's  ({len(text4)} chars)")
    print(f"  Compressed: {comp4!r}  ({len(comp4)} bytes)")
    print(f"  RLE pairs : {format_rle(comp4)}")
    print(f"  Decompressed length: {len(decomp4)}")
    print(f"  Round-trip OK: {text4 == decomp4}")

    # ---- Binary example 1: Repeated byte values --------------------------
    binary1 = bytes([0x00, 0x00, 0x00, 0xFF, 0xFF, 0x01, 0x01, 0x01, 0x01])
    comp_bin1 = rle_compress(binary1)
    decomp_bin1 = rle_decompress(comp_bin1)

    print(f"\n--- Binary Example 1: Mixed byte values ---")
    print(f"  Original  : {binary1!r}")
    print(f"  Compressed: {comp_bin1!r}  ({len(comp_bin1)} bytes)")
    print(f"  RLE pairs : {format_rle(comp_bin1)}")
    print(f"  Decompressed: {decomp_bin1!r}")
    print(f"  Round-trip OK: {binary1 == decomp_bin1}")

    # ---- Binary example 2: All zeros (common in binary data) ------------
    binary2 = bytes([0x00] * 500)
    comp_bin2 = rle_compress(binary2)
    decomp_bin2 = rle_decompress(comp_bin2)

    print(f"\n--- Binary Example 2: 500 zero bytes ---")
    print(f"  Original  : 500 zero bytes")
    print(f"  Compressed: {comp_bin2!r}  ({len(comp_bin2)} bytes)")
    print(f"  RLE pairs : {format_rle(comp_bin2)}")
    print(f"  Decompressed length: {len(decomp_bin2)}")
    print(f"  Round-trip OK: {binary2 == decomp_bin2}")
    print(f"  Compression ratio: {len(comp_bin2) / len(binary2):.2%}")

    # ---- Binary example 3: Raw binary data with no runs ------------------
    binary3 = bytes(range(256))
    comp_bin3 = rle_compress(binary3)
    decomp_bin3 = rle_decompress(comp_bin3)

    print(f"\n--- Binary Example 3: All unique bytes (worst case) ---")
    print(f"  Original  : 256 unique bytes")
    print(f"  Compressed: {len(comp_bin3)} bytes")
    print(f"  RLE pairs : {format_rle(comp_bin3)}")
    print(f"  Round-trip OK: {binary3 == decomp_bin3}")
    print(f"  Note: Data doubles in size (2 bytes per input byte).")

    # ---- Summary ----------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print("""
Run-length encoding works well when data contains long runs of
repeated values (e.g., simple graphics, sparse binary data, DNA
sequences).  It is not effective — and actually expands — data
with few or no repeated values.

Key properties:
  • Lossless: original data is perfectly recovered.
  • Simple: very fast encode/decode, minimal memory.
  • Format: each run = 2 bytes [count (1-255), value].
  • Longest single run: 255 bytes (split into multiple segments).
""")
