import matplotlib.pyplot as plt
import networkx as nx

# 한글 폰트 설정 (환경에 맞게 해제하여 사용)
plt.rcParams['font.family'] = 'sans-serif' 
# plt.rcParams['font.family'] = 'Malgun Gothic' # Windows
# plt.rcParams['font.family'] = 'AppleGothic' # Mac

def draw_case_study_analysis_vertical():
    # ---------------------------------------------------------
    # 데이터 설정
    # ---------------------------------------------------------
    models = ['Analysis 1: Ideal Model\n(Rational Choice)', 'Analysis 2: Blind Model\n(Partisan Voting)']
    utilities = [90, 10] 
    candidates_chosen = ['vB (Different Party, High Ethics)', 'vA (Same Party, Low Ethics)']
    colors = ['#2e7d32', '#c62828'] 

    # [수정됨] 2행 1열 구조로 변경, 크기는 세로로 길게 (10, 12)
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))

    # ---------------------------------------------------------
    # 그래프 1: 매칭 구조 시각화 (Network Diagram) - 위쪽
    # ---------------------------------------------------------
    ax1 = axes[0]
    G = nx.Graph()
    
    # 노드 위치 조정 (세로 배치에 맞게 조금 더 넓게 퍼뜨림)
    G.add_node('u1', pos=(0, 0.5), label='Voter u1\n(Party A, Values Ethics)')
    G.add_node('vA', pos=(1, 0.8), label='Candidate vA\n(Party A, Ethics=10)')
    G.add_node('vB', pos=(1, 0.2), label='Candidate vB\n(Party B, Ethics=90)')
    
    pos = nx.get_node_attributes(G, 'pos')
    
    # 노드 그리기
    nx.draw_networkx_nodes(G, pos, ax=ax1, node_size=3000, node_color=['#FFF59D', '#FFCDD2', '#C8E6C9'], edgecolors='black')
    
    # 엣지 그리기
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=[('u1', 'vB')], 
                           width=3, edge_color='green', style='dashed', connectionstyle="arc3,rad=-0.1")
    nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=[('u1', 'vA')], 
                           width=3, edge_color='red', style='solid', connectionstyle="arc3,rad=0.1")
    
    # 라벨
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, ax=ax1, font_size=11)
    
    # 설명 텍스트
    ax1.text(0.5, 0.72, "Blind Choice (Same Party)", color='red', fontsize=12, ha='center', fontweight='bold', rotation=12)
    ax1.text(0.5, 0.28, "Ideal Choice (High Ethics)", color='green', fontsize=12, ha='center', fontweight='bold', rotation=-12)
    
    ax1.set_title("[Graph 1] Matching Choices in Two Models", fontsize=16, pad=20)
    ax1.axis('off')

    # ---------------------------------------------------------
    # 그래프 2: 효용 비교 (Bar Chart) - 아래쪽
    # ---------------------------------------------------------
    ax2 = axes[1]
    bars = ax2.bar(models, utilities, color=colors, alpha=0.8, width=0.4)
    
    for bar, score, choice in zip(bars, utilities, candidates_chosen):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, height - 8, f'Utility: {score}', 
                 ha='center', va='bottom', color='white', fontweight='bold', fontsize=14)
        ax2.text(bar.get_x() + bar.get_width()/2.0, height + 3, f'Chose: {choice}', 
                 ha='center', va='bottom', color='black', fontsize=11)

    ax2.set_ylim(0, 115)
    ax2.set_ylabel('Voter Satisfaction (Utility)', fontsize=13)
    ax2.set_title("[Graph 2] Social Welfare Comparison", fontsize=16, pad=15)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    # 텍스트 박스 위치 조정
    text_box = (f"Partisanship Cost (Loss) = {utilities[0] - utilities[1]}\n"
                "Blind voting leads to a massive drop in social welfare.")
    ax2.text(0.5, 60, text_box, fontsize=13, ha='center', bbox=dict(boxstyle="round", fc="white", ec="black"))

    plt.tight_layout()
    plt.show()

# 실행
draw_case_study_analysis_vertical()
