"""XGLCD Font Utility."""
from math import floor


class XglcdFont(object):
    """Font data in X-GLCD format.

    Attributes:
        letters: A bytearray of letters (columns consist of bytes)
        width: Maximum pixel width of font
        height: Pixel height of font
        start_letter: ASCII number of first letter
        height_bytes: How many bytes comprises letter height

    Note:
        Font files can be generated with the free version of MikroElektronika
        GLCD Font Creator:  www.mikroe.com/glcd-font-creator
        The font file must be in X-GLCD 'C' format.
        To save text files from this font creator program in Win7 or higher
        you must use XP compatibility mode or you can just use the clipboard.
    """

    # Dict to translate bitwise values to byte position
    BIT_POS = {1: 0, 2: 2, 4: 4, 8: 6, 16: 8, 32: 10, 64: 12, 128: 14, 256: 16}
    # Dict to translate bitwise values to byte position (for transparent)
    BIT_POS_T = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8}

    def __init__(self, path, width, height, start_letter=32, letter_count=96):
        """Constructor for X-GLCD Font object.

        Args:
            path (string): Full path of font file
            width (int): Maximum width in pixels of each letter
            height (int): Height in pixels of each letter
            start_letter (int): First ACII letter.  Default is 32.
            letter_count (int): Total number of letters.  Default is 96.
        """
        self.width = width
        self.height = height
        self.start_letter = start_letter
        self.letter_count = letter_count
        self.bytes_per_letter = (floor(
            (self.height - 1) / 8) + 1) * self.width + 1
        self.__load_xglcd_font(path)

    def __load_xglcd_font(self, path):
        """Load X-GLCD font data from text file.

        Args:
            path (string): Full path of font file.
        """
        bytes_per_letter = self.bytes_per_letter
        # Buffer to hold letter byte values
        self.letters = bytearray(bytes_per_letter * self.letter_count)
        mv = memoryview(self.letters)
        offset = 0
        with open(path, 'r') as f:
            for line in f:
                # Skip lines that do not start with hex values
                line = line.strip()
                if len(line) == 0 or line[0:2] != '0x':
                    continue
                # Remove comments
                comment = line.find('//')
                if comment != -1:
                    line = line[0:comment].strip()
                # Remove trailing commas
                if line.endswith(','):
                    line = line[0:len(line) - 1]
                # Convert hex strings to bytearray and insert in to letters
                mv[offset: offset + bytes_per_letter] = bytearray(
                    int(b, 16) for b in line.split(','))
                offset += bytes_per_letter

    def lit_bits(self, n):
        """Return positions of 1 bits only."""
        while n:
            b = n & (~n+1)
            yield self.BIT_POS[b]
            n ^= b

    def lit_bits_t(self, n):
        """Return positions of 1 bits only (transparent)."""
        while n:
            b = n & (~n+1)
            yield self.BIT_POS_T[b]
            n ^= b

    def get_width_height(self, letter):
        """Return width and height of letter."""
        # Get index of letter
        letter_ord = ord(letter) - self.start_letter
        # Confirm font contains letter
        if letter_ord >= self.letter_count:
            print('Font does not contain character: ' + letter)
            return 0, 0
        bytes_per_letter = self.bytes_per_letter
        offset = letter_ord * bytes_per_letter
        return self.letters[offset], self.height

    def get_letter(self, letter, color, background=0, landscape=False):
        """Convert letter byte data to pixels.

        Args:
            letter (string): Letter to return (must exist within font).
            color (int): RGB565 color value.
            background (int): RGB565 background color (default: black).
            landscape (bool): Orientation (default: False = portrait)
        Returns:
            (bytearray): Pixel data.
            (int, int): Letter width and height.
        """
        # Get index of letter
        letter_ord = ord(letter) - self.start_letter
        # Confirm font contains letter
        if letter_ord >= self.letter_count:
            print('Font does not contain character: ' + letter)
            return b'', 0, 0
        bytes_per_letter = self.bytes_per_letter
        offset = letter_ord * bytes_per_letter
        mv = memoryview(self.letters[offset:offset + bytes_per_letter])

        # Get width of letter (specified by first byte)
        letter_width = mv[0]
        letter_height = self.height
        # Get size in bytes of specified letter
        letter_size = letter_height * letter_width
        # Create buffer (double size to accommodate 16 bit colors)
        if background:
            buf = bytearray(background.to_bytes(2, 'big') * letter_size)
        else:
            buf = bytearray(letter_size * 2)

        msb, lsb = color.to_bytes(2, 'big')

        column_size = letter_height * 2
        if landscape:
            # Populate starting at end of each column
            pos = column_size - 1
        else:
            # Populate buffer in order for portrait
            pos = 0
        lh = letter_height
        start_pos = pos
        # Loop through letter byte data and convert to pixel data
        for b in mv[1:]:
            # Process only colored bits
            for bit in self.lit_bits(b):
                if landscape:
                    # print("lh: {}, pos: {}, bit: {}".format(lh, pos, bit))
                    buf[pos - (bit + 1)] = msb
                    buf[pos - bit] = lsb
                else:
                    # print("lh: {}, pos: {}, bit: {}".format(lh, pos, bit))
                    buf[bit + pos] = msb
                    buf[bit + pos + 1] = lsb
            if lh > 8:
                if landscape:
                    # Decrement position by double byte
                    pos -= 16
                else:
                    # Increment position by double byte
                    pos += 16
                lh -= 8
            else:
                if landscape:
                    # Move position to end of next row
                    pos = start_pos + column_size
                    start_pos = pos
                else:
                    # Increase position by remaing letter height to next column
                    pos += lh * 2
                lh = letter_height
        return buf, letter_width, letter_height

    def get_letter_trans(self, letter, landscape=False):
        """Convert letter byte data to X,Y pixels for transparent drawing.

        Args:
            letter (string): Letter to return (must exist within font).
            landscape (bool): Orientation (default: False = portrait)
        Yields:
            (int, int): X,Y relative position of bits to draw
        """
        # Get index of letter
        letter_ord = ord(letter) - self.start_letter
        # Confirm font contains letter
        if letter_ord >= self.letter_count:
            print('Font does not contain character: ' + letter)
            return b'', 0, 0
        bytes_per_letter = self.bytes_per_letter
        offset = letter_ord * bytes_per_letter
        mv = memoryview(self.letters[offset:offset + bytes_per_letter])

        # Get width of letter (specified by first byte)
        letter_height = self.height
        x = 0

        # Determine number of bytes per letter Y column
        byte_height = int(letter_height / 8) + (letter_height % 8 > 0)
        bh = 0
        # Loop through letter byte data and convert to pixel data
        for b in mv[1:]:
            # Process only colored bits
            for bit in self.lit_bits_t(b):
                if landscape:
                    yield letter_height - ((bh << 3) + bit), x
                else:
                    yield x, (bh << 3) + bit
            if bh < byte_height - 1:
                # Next column byte
                bh += 1
            else:
                # Next column
                x += 1
                bh = 0

    def measure_text(self, text, spacing=1):
        """Measure length of text string in pixels.

        Args:
            text (string): Text string to measure
            spacing (optional int): Pixel spacing between letters.  Default: 1.
        Returns:
            int: length of text
        """
        length = 0
        for letter in text:
            # Get index of letter
            letter_ord = ord(letter) - self.start_letter
            offset = letter_ord * self.bytes_per_letter
            # Add length of letter and spacing
            length += self.letters[offset] + spacing
        return length