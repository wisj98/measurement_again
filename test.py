def find_last_plus_and_k(text):
  """
  긴 문자열에서 마지막 k를 찾고, 그 마지막 k 전까지 나온 + 중 가장 마지막 +의 위치를 알려주는 함수

  Args:
    text: 긴 길이의 문자열

  Returns:
    마지막 k 전까지 나온 + 중 가장 마지막 +의 위치와 마지막 k의 위치. 
    만약 해당하는 + 또는 k가 없으면 -1을 반환합니다.
  """
  last_k_index = text.rfind("k")  # 마지막 k의 인덱스 찾기
  if last_k_index == -1:  # k가 없으면 -1 반환
    return -1, -1

  last_plus_index = text.rfind("+", 0, last_k_index)  # 마지막 k 이전의 + 인덱스 찾기
  return last_plus_index, last_k_index

# 예시
text = "abcdef+ghijk+lmnokpqrs+tuvwkxyz"
plus_index, k_index = find_last_plus_and_k(text)
print(f"+의 위치: {plus_index}, k의 위치: {k_index}")
print(text[plus_index+1:k_index])