import re

def test(text):
  j = 0
  while True:
    if j >= len(text):
      break
    text[j] = text[j].strip()

    pattern = r"\b\d{1,3}\.\s\(?([A-Za-z])\)?\s*"

    match = re.search(pattern, text[j])
    if match:
      text[j] = match.group(1)
    elif len(text[j]) != 1 or not text[j][-1].isalpha():
      text.pop(j)
      continue

    text[j] = text[j][-1].lower()
    if text[j] not in 'abcde':
      text.pop(j)
      continue
    j += 1
  print(text)

test(['1. A', '2. A', '3. A', '4. A', '5. A', '6. A', '7. B', '8. B', '9. A', '10. A'])