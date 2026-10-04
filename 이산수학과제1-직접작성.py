def input_matrix():
    """1. 행렬 입력 기능 (n x n 크기의 정방행렬을 행 단위로 입력)"""
    n = int(input("정수 n을 입력하세요 (n x n 정방행렬): "))
    matrix = []
    print(f"-> {n}개의 숫자를 공백으로 구분하여 각 행을 입력해주세요.")
    for i in range(n):
        while True:
            try:
                row = list(map(float, input(f"행 {i + 1} 입력: ").split()))
                if len(row) != n:
                    print("오류: 정확히 n개의 숫자를 입력해야 합니다.다시 입력하세요.")
                    continue
                matrix.append(row)
                break
            except ValueError:
                print("오류: 올바른 숫자를 입력해주세요.")
    return n, matrix


def get_minor(matrix, i, j):
    """행 i와 열 j를 제외한 소행렬(Minor) 반환"""
    return [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]


def calculate_determinant(matrix):
    """재귀적 여인수 전개를 통한 행렬식 계산"""
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(n):
        sign = (-1) ** c
        det += sign * matrix[0][c] * calculate_determinant(get_minor(matrix, 0, c))
    return det


def inverse_by_determinant(matrix):
    """2. 행렬식(여인수 및 수반행렬)을 이용한 역행렬 계산 함수"""
    n = len(matrix)
    det = calculate_determinant(matrix)

    # 예외 처리: 행렬식이 0인 경우
    if abs(det) < 1e-9:
        raise ValueError("오류 [행렬식 방식]: 행렬식이 0이므로 역행렬이 존재하지 않습니다.")

    if n == 1:
        return [[1.0 / matrix[0][0]]]

    # 여인수 행렬 계산
    cofactors = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            minor = get_minor(matrix, r, c)
            sign = (-1) ** (r + c)
            cofactor_row.append(sign * calculate_determinant(minor))
        cofactors.append(cofactor_row)

    # 수반행렬(Adjugate)은 여인수 행렬의 전치
    adjugate = [[cofactors[c][r] for c in range(n)] for r in range(n)]

    # 역행렬 = (1 / det) * 수반행렬
    inverse = [[adjugate[r][c] / det for c in range(n)] for r in range(n)]
    return inverse


def inverse_by_gauss_jordan(matrix):
    """3. 가우스-조던 소거법을 이용한 역행렬 계산 함수"""
    n = len(matrix)
    # [A | I] 확장 행렬 생성
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]

    for i in range(n):
        # 부분 피벗팅(Partial Pivoting)
        max_row = i
        for r in range(i + 1, n):
            if abs(m[r][i]) > abs(m[max_row][i]):
                max_row = r
        m[i], m[max_row] = m[max_row], m[i]

        # 예외 처리: 피벗이 0인 경우 (역행렬 없음)
        if abs(m[i][i]) < 1e-9:
            raise ValueError("오류 [가우스-조던 방식]: 피벗이 0이 되어 역행렬이 존재하지 않습니다.")

        pivot = m[i][i]
        m[i] = [val / pivot for val in m[i]]

        for r in range(n):
            if r != i:
                factor = m[r][i]
                m[r] = [m[r][c] - factor * m[i][c] for c in range(2 * n)]

    return [row[n:] for row in m]


def compare_and_print(inv1, inv2):
    """4. 결과 출력 및 비교 기능"""
    n = len(inv1)
    print("\n" + "=" * 40)
    print(" [결과 1] 행렬식 방식을 이용한 역행렬")
    print("=" * 40)
    for r in inv1:
        print([round(x, 4) for x in r])

    print("\n" + "=" * 40)
    print(" [결과 2] 가우스-조던 소거법을 이용한 역행렬")
    print("=" * 40)
    for r in inv2:
        print([round(x, 4) for x in r])

    # 비교 검증
    match = all(abs(inv1[i][j] - inv2[i][j]) < 1e-6 for i in range(n) for j in range(n))

    print("\n" + "=" * 40)
    print(" [결과 3] 두 방법 비교 메시지")
    print("=" * 40)
    if match:
        print("결과: 두 방법으로 계산한 역행렬이 동일합니다")
    else:
        print("결과: 두 방법으로 계산한 역행렬이 다릅니다")


def verify_inverse_multiplication(original, inverse):
    """[추가 기능] 역행렬 검증 기능: 원본 행렬과 역행렬의 곱(A * A^-1)이 단위행렬(I)이 되는지 확인"""
    n = len(original)
    identity_check = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            val = sum(original[i][k] * inverse[k][j] for k in range(n))
            identity_check[i][j] = round(val, 0) if abs(val - round(val)) < 1e-4 else round(val, 4)

    print("\n" + "=" * 40)
    print(" [추가 기능] 역행렬 검증 (A × A⁻¹ = 단위행렬 확인)")
    print("=" * 40)
    for r in identity_check:
        print(r)


if __name__ == "__main__":
    try:
        # 1.행렬 입력
        n, matrix = input_matrix()

        # 2.행렬식 방식 역행렬 계산
        inv_det = inverse_by_determinant(matrix)

        # 3.가우스-조던 소거법 역행렬 계산
        inv_gj = inverse_by_gauss_jordan(matrix)

        # 4.결과 출력 및 비교
        compare_and_print(inv_det, inv_gj)

        # 추가 기능 실행 (역행렬 검증)
        verify_inverse_multiplication(matrix, inv_gj)

    except ValueError as e:
        print("\n[예외 발생]", e)