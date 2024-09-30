import urllib.parse

raw_data = """
<script>
    var ws = new WebSocket('wss://0af0003304110508804f303b00390059.web-security-academy.net/chat');
    ws.onopen = function();
</script>
"""

# Full URL encode (encoding all characters)
encoded_data = urllib.parse.quote(raw_data, safe='')

print(encoded_data)
