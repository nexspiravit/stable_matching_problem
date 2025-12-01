import numpy as np
import matplotlib.pyplot as plt
import random

# ==========================================
# 1. 클래스 및 효용 함수 정의
# ==========================================

class Candidate:
    def __init__(self, id, party, policy_pos, ethics):
        self.id = id
        self.party = party          # 0: A당, 1: B당
        self.policy_pos = policy_pos # 0.0 ~ 1.0 (정책 스펙트럼)
        self.ethics = ethics        # 0 ~ 100 (윤리 점수)

class Voter:
    def __init__(self, id, party, policy_pref):
        self.id = id
        self.party = party          # 0: A당, 1: B당
        self.policy_pref = policy_pref # 0.0 ~ 1.0

def calculate_ideal_utility(voter, candidate, alpha=1.0, beta=0.5):
    """
    [이상적 효용 함수] 정책 거리의 역수와 윤리 점수를 고려
    """
    distance = abs(voter.policy_pref - candidate.policy_pos)
    # 거리가 0일 때 무한대 방지를 위해 epsilon(0.01) 추가
    policy_score = 1.0 / (distance + 0.01)
    ethics_score = candidate.ethics
    return (alpha * policy_score) + (beta * ethics_score)

def calculate_blind_utility(voter, candidate):
    """
    [맹목적 효용 함수] 정당이 같으면 무조건 선택
    """
    if voter.party == candidate.party:
        return 99999.0 # 무한대에 가까운 상수
    else:
        return 0.0

# ==========================================
# 2. 데이터 생성 (초기 설정)
# ==========================================

# 시드 고정
np.random.seed(42)
random.seed(42)

# 후보자 생성
# 후보 A: A당, 정책 극단(0.1), 윤리 최악(10점) -> "나쁜 후보"
# 후보 B: B당, 정책 중도(0.6), 윤리 최상(90점) -> "좋은 후보"
candidates = [
    Candidate(id='C_A', party=0, policy_pos=0.1, ethics=10), 
    Candidate(id='C_B', party=1, policy_pos=0.6, ethics=90)
]

# 유권자 생성 (100명)
voters = []
for i in range(100):
    pref = np.random.rand() 
    party = np.random.randint(0, 2)
    voters.append(Voter(id=i, party=party, policy_pref=pref))

# ==========================================
# 3. 기준값 계산 (이상적 상황의 총 효용)
# ==========================================

def run_election_once(voters, candidates, mode='ideal'):
    total_social_welfare = 0
    for voter in voters:
        best_candidate = None
        max_utility = -1.0
        
        # 투표(선택) 과정
        for candidate in candidates:
            if mode == 'ideal':
                util = calculate_ideal_utility(voter, candidate)
            elif mode == 'blind':
                util = calculate_blind_utility(voter, candidate)
            
            if util > max_utility:
                max_utility = util
                best_candidate = candidate
        
        # 실제 효용(행복)은 항상 '이상적 기준'으로 계산
        real_welfare = calculate_ideal_utility(voter, best_candidate)
        total_social_welfare += real_welfare
        
    return total_social_welfare

# 100% 이상적일 때의 사회 후생 총합 (기준점)
welfare_ideal = run_election_once(voters, candidates, mode='ideal')

print(f"이상적 환경에서의 최대 사회 후생: {welfare_ideal:.2f}")

# ==========================================
# 4. 시뮬레이션 및 시각화 실행
# ==========================================

def simulate_partisanship_impact():
    welfare_losses = []
    # 0% ~ 100% 까지 맹목적 투표 비율을 20단계로 나눔
    ratios = np.linspace(0, 1.0, 20) 
    
    print("\n시뮬레이션 진행 중...", end="")
    
    for ratio in ratios:
        current_welfare_sum = 0
        
        # 유권자들 중 ratio 비율만큼은 맹목적 투표자가 됨
        for voter in voters:
            is_blind = np.random.rand() < ratio # 확률적으로 맹목적 여부 결정
            
            best_candidate = None
            max_utility = -1.0
            
            for candidate in candidates:
                # 맹목적 유권자는 blind 함수, 합리적 유권자는 ideal 함수 사용
                if is_blind:
                    util = calculate_blind_utility(voter, candidate)
                else:
                    util = calculate_ideal_utility(voter, candidate)
                
                if util > max_utility:
                    max_utility = util
                    best_candidate = candidate
            
            # 매칭 결과에 따른 실제 효용 누적
            real_welfare = calculate_ideal_utility(voter, best_candidate)
            current_welfare_sum += real_welfare
            
        # 손실값(비용) = 최대 가능 효용 - 현재 효용
        loss = welfare_ideal - current_welfare_sum
        welfare_losses.append(loss)
        print(".", end="") # 진행 표시

    print(" 완료!\n")

    # 그래프 그리기
    plt.figure(figsize=(10, 6))
    
    # 꺾은선 그래프
    plt.plot(ratios * 100, welfare_losses, marker='o', color='red', linestyle='-', linewidth=2, label='Social Cost')
    
    # 그래프 꾸미기
    plt.title('Increase in Social Cost due to Blind Partisan Voting', fontsize=15, fontweight='bold')
    plt.xlabel('Ratio of Blind Partisan Voters (%)', fontsize=12)
    plt.ylabel('Social Welfare Loss (Cost)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 영역 채우기
    plt.fill_between(ratios * 100, welfare_losses, color='red', alpha=0.1)
    
    # 텍스트 추가 (우상향 강조)
    plt.text(50, max(welfare_losses)/2, "Partisanship Cost Gap", fontsize=12, color='darkred', ha='center')

    plt.tight_layout()
    plt.show()

# 함수 실행
if __name__ == "__main__":
    simulate_partisanship_impact()
