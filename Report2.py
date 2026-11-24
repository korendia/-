from copy import deepcopy

ELEMENTS = [1, 2, 3, 4, 5]
N = len(ELEMENTS)


def print_matrix(matrix, title=None):
    """5x5 관계 행렬을 보기 좋게 출력합니다."""
    if title:
        print(f"\n[{title}]")
    header = "    " + " ".join(str(e) for e in ELEMENTS)
    print(header)
    print("   " + "-" * (N * 2 + 1))
    for i, row in enumerate(matrix):
        row_str = " ".join(str(val) for val in row)
        print(f" {ELEMENTS[i]} | {row_str}")


# 1. 관계 행렬 입력 기능
def input_relation_matrix():
    """사용자로부터 5x5 관계 행렬을 행 단위로 입력받아 2차원 리스트로 반환합니다."""
    print("\n집합 A = {1, 2, 3, 4, 5}에 대한 5 x 5 관계 행렬을 행 단위로 입력하세요.")
    print("(각 행은 0 또는 1을 공백으로 구분하여 5개 입력, 예: 1 0 0 0 0)")
    matrix = []

    for i in range(N):
        while True:
            raw = input(f"{i + 1}행 입력: ").strip()
            parts = raw.split()
            if len(parts) != N:
                print(f"  [오류] 정확히 {N}개의 값을 공백으로 구분해 입력해야 합니다.")
                continue
            if not all(p in ("0", "1") for p in parts):
                print("  [오류] 0 또는 1만 입력할 수 있습니다.")
                continue
            matrix.append([int(p) for p in parts])
            break

    return matrix


# 2. 동치 관계 판별 기능 (반사, 대칭, 추이)
def is_reflexive(matrix):
    """반사 관계 여부와 누락된 대각 쌍(반례)을 반환합니다."""
    violations = []
    for i in range(N):
        if matrix[i][i] != 1:
            violations.append((ELEMENTS[i], ELEMENTS[i]))
    return len(violations) == 0, violations


def is_symmetric(matrix):
    """대칭 관계 여부와 대칭쌍이 누락된 순서쌍(반례)을 반환합니다."""
    violations = []
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1 and matrix[j][i] != 1:
                violations.append((ELEMENTS[i], ELEMENTS[j]))
    return len(violations) == 0, violations


def is_transitive(matrix):
    """추이 관계 여부와 위배된 순서쌍(반례)을 반환합니다."""
    violations = []
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                for k in range(N):
                    if matrix[j][k] == 1 and matrix[i][k] != 1:
                        violations.append((ELEMENTS[i], ELEMENTS[j], ELEMENTS[k]))
    return len(violations) == 0, violations


def is_antisymmetric(matrix):
    """[추가 기능] 반대칭 관계 여부를 판별합니다."""
    for i in range(N):
        for j in range(N):
            if i != j and matrix[i][j] == 1 and matrix[j][i] == 1:
                return False
    return True


def check_equivalence_relation(matrix):
    """반사, 대칭, 추이 관계를 판별하고 결과를 출력한 뒤 동치 관계 여부를 반환합니다."""
    ref, ref_v = is_reflexive(matrix)
    sym, sym_v = is_symmetric(matrix)
    tra, tra_v = is_transitive(matrix)
    anti = is_antisymmetric(matrix)

    print("\n=== 관계 성질 판별 결과 ===")
    print(f"- 반사 관계(Reflexive): {'성립 (O)' if ref else '성립 안 함 (X)'}")
    if not ref:
        print(f"    -> 누락된 대각 쌍: {ref_v}")

    print(f"- 대칭 관계: {'성립 (O)' if sym else '성립 안 함 (X)'}")
    if not sym:
        print(f"    -> 대칭쌍 누락 (a, b) 목록: {sym_v}")

    print(f"- 추이 관계: {'성립 (O)' if tra else '성립 안 함 (X)'}")
    if not tra:
        sample = tra_v[:5]
        suffix = f" 외 {len(tra_v) - 5}건" if len(tra_v) > 5 else ""
        print(f"    -> 추이 위배 (a, b, c) 예시: {sample}{suffix}")

    print(f"- [참고] 반대칭 관계: {'성립 (O)' if anti else '성립 안 함 (X)'}")

    is_equiv = ref and sym and tra
    if is_equiv:
        print("\n>> 판별 결과: 이 관계는 '동치 관계'입니다.")
    else:
        print("\n>> 판별 결과: 이 관계는 '동치 관계'가 아닙니다.")

    return is_equiv, ref, sym, tra


# 3. 동치류 출력 기능
def get_equivalence_class(matrix, element):
    """특정 원소 element의 동치류 [element]를 리스트로 반환합니다."""
    idx = ELEMENTS.index(element)
    return [ELEMENTS[j] for j in range(N) if matrix[idx][j] == 1]


def print_equivalence_classes(matrix):
    """집합 A의 모든 원소에 대한 동치류와 분할(몫집합)을 출력합니다."""
    print("\n=== 동치류 출력 ===")
    unique_classes = []
    for e in ELEMENTS:
        eq_class = get_equivalence_class(matrix, e)
        class_str = ", ".join(str(x) for x in eq_class)
        print(f"[{e}] = {{{class_str}}}")
        if eq_class not in unique_classes:
            unique_classes.append(eq_class)

    partition_str = ", ".join(
        "{" + ", ".join(str(x) for x in cls) + "}" for cls in unique_classes
    )
    print(f"\n[추가 기능] 집합 A의 분할 (몫집합 A/R): {{{partition_str}}}")


# 4. 폐포 구현 기능 (반사 폐포, 대칭 폐포, 추이 폐포)
def reflexive_closure(matrix):
    """반사 폐포를 생성하여 반환합니다."""
    result = deepcopy(matrix)
    for i in range(N):
        result[i][i] = 1
    return result


def symmetric_closure(matrix):
    """대칭 폐포를 생성하여 반환합니다."""
    result = deepcopy(matrix)
    for i in range(N):
        for j in range(N):
            if result[i][j] == 1:
                result[j][i] = 1
    return result


def transitive_closure(matrix):
    """추이 폐포를 생성하여 반환합니다."""
    result = deepcopy(matrix)
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if result[i][k] == 1 and result[k][j] == 1:
                    result[i][j] = 1
    return result


# [추가 기능] 관계 순서쌍 출력
def print_relation_pairs(matrix):
    """관계 행렬을 순서쌍 집합 R 형태로 출력합니다."""
    pairs = [
        f"({ELEMENTS[i]}, {ELEMENTS[j]})"
        for i in range(N)
        for j in range(N)
        if matrix[i][j] == 1
    ]
    print(f"\n[추가 기능] 순서쌍 표현 R = {{{', '.join(pairs)}}}")


def process_relation(matrix):
    """동치 관계 판별 -> 동치류 출력 또는 폐포 변환 후 재판별을 수행합니다."""
    print_matrix(matrix, "입력된 관계 행렬")
    print_relation_pairs(matrix)

    is_equiv, ref, sym, tra = check_equivalence_relation(matrix)

    if is_equiv:
        print_equivalence_classes(matrix)
        return

    # 반사 -> 대칭 -> 추이 순으로 필요한 폐포를 순차 적용
    print("\n=== 폐포 변환 진행 ===")
    current = deepcopy(matrix)

    if not ref:
        print("\n[1] 반사 관계가 아니므로 반사 폐포를 적용합니다.")
        print_matrix(current, "반사 폐포 변환 전")
        current = reflexive_closure(current)
        print_matrix(current, "반사 폐포 변환 후")

    sym_now, _ = is_symmetric(current)
    if not sym_now:
        print("\n[2] 대칭 관계가 아니므로 대칭 폐포를 적용합니다.")
        print_matrix(current, "대칭 폐포 변환 전")
        current = symmetric_closure(current)
        print_matrix(current, "대칭 폐포 변환 후")

    tra_now, _ = is_transitive(current)
    if not tra_now:
        print("\n[3] 추이 관계가 아니므로 추이 폐포를 적용합니다.")
        print_matrix(current, "추이 폐포 변환 전")
        current = transitive_closure(current)
        print_matrix(current, "추이 폐포 변환 후")

    print("\n=== 폐포 변환 후 동치 관계 재판별 ===")
    print_matrix(current, "최종 변환된 관계 행렬")
    print_relation_pairs(current)
    is_equiv_after, _, _, _ = check_equivalence_relation(current)

    if is_equiv_after:
        print_equivalence_classes(current)


def main():
    sample_equiv = [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    sample_non_equiv = [
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
    ]

    while True:
        print("\n=========================================")
        print("  동치 관계 판별 및 폐포 변환 프로그램")
        print("=========================================")
        print("1. 5 x 5 관계 행렬 직접 입력")
        print("2. [예제 1] 동치 관계 행렬 테스트")
        print("3. [예제 2] 비동치 관계 행렬(폐포 변환) 테스트")
        print("0. 종료")
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "1":
            matrix = input_relation_matrix()
            process_relation(matrix)
        elif choice == "2":
            process_relation(sample_equiv)
        elif choice == "3":
            process_relation(sample_non_equiv)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("[오류] 0~3 사이의 번호를 입력해 주세요.")


if __name__ == "__main__":
    main()
