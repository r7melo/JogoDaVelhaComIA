import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.board import Board
from src.models.alpha_beta import AlphaBeta
from src.models.minimax import Minimax

REPETICOES = 10

CONFIG_BOARDS = {
    "E1": ["", "", "", "", "", "", "", "", ""],                 # tabuleiro vazio
    "E2": ["", "", "", "", "X", "", "", "", ""],                 # X abriu no centro
    "E3": ["X", "", "", "", "O", "", "", "", ""],                # jogo aberto
    "E4": ["X", "O", "", "X", "O", "", "", "", ""],              # meio de jogo
    "E5": ["X", "O", "X", "O", "X", "O", "", "", ""],            # final de jogo
}

# Estado usado no teste de inversao de ordem de geracao de jogadas.
ESTADO_INVERSAO = "E4"


def board_from_cells(cells: list) -> Board:
    board = Board()
    for pos, simbolo in enumerate(cells):
        if simbolo in ("X", "O"):
            board.set_play(pos, simbolo)
    return board


def jogador_da_vez(cells: list) -> str:
    qtd_x = cells.count("X")
    qtd_o = cells.count("O")
    return "X" if qtd_x == qtd_o else "O"


def format_board(cells: list) -> str:
    def c(v):
        return v if v else "_"
    linhas = ["".join(c(v) for v in cells[i:i + 3]) for i in (0, 3, 6)]
    return " | ".join(linhas)


def run_repeated(cls, board: Board, player: str, reverse: bool = False,
                  repeticoes: int = REPETICOES):
    posicao = valor = nos = None
    tempos = []
    for _ in range(repeticoes):
        agente = cls(board, player, reverse=reverse)
        d = agente.best_decision()
        tempos.append(d.time_ms)
        posicao, valor, nos = d.position, int(d.value), d.nodes
    tempo_medio = statistics.mean(tempos)
    return posicao, valor, nos, tempo_medio


def main() -> None:
    estados = list(CONFIG_BOARDS.items())

    # valida que os estados nao sao terminais
    for nome, cells in estados:
        board = board_from_cells(cells)
        tem_vencedor, _ = board.has_winner()
        if tem_vencedor or board.is_end_game():
            raise ValueError(f"{nome}: tabuleiro e terminal, escolha outro estado")

    linhas_csv = []
    cabecalho = f"{'Estado':8}{'Algoritmo':12}{'Jogada':8}{'Valor':8}{'Nos':10}{'Tempo medio (ms)':18}"
    print(cabecalho)
    print("-" * len(cabecalho))

    for nome, cells in estados:
        board = board_from_cells(cells)
        turno = jogador_da_vez(cells)

        pos_mm, val_mm, nos_mm, t_mm = run_repeated(Minimax, board, turno)
        pos_ab, val_ab, nos_ab, t_ab = run_repeated(AlphaBeta, board, turno)

        reducao = (nos_mm - nos_ab) / nos_mm * 100 if nos_mm else 0.0

        print(f"{nome:8}{'Minimax':12}{pos_mm:<8}{val_mm:<+8}{nos_mm:<10}{t_mm:<18.3f}")
        print(f"{nome:8}{'Alfa-beta':12}{pos_ab:<8}{val_ab:<+8}{nos_ab:<10}{t_ab:<18.3f}")
        print(f"        tabuleiro: {format_board(cells)}  (vez de {turno})")
        print(f"        reducao de nos (alfa-beta vs minimax): {reducao:.2f}%\n")

        linhas_csv.append([nome, turno, "Minimax", pos_mm, val_mm, nos_mm, round(t_mm, 4)])
        linhas_csv.append([nome, turno, "Alfa-beta", pos_ab, val_ab, nos_ab, round(t_ab, 4)])

    csv_path = Path(__file__).resolve().parent / "benchmark_resultados.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Estado", "Jogador_da_vez", "Algoritmo",
                          "Jogada", "Valor", "Nos", "Tempo_medio_ms"])
        writer.writerows(linhas_csv)
    print(f"Resultados salvos em: {csv_path}\n")

    # --- teste de inversao da ordem de geracao de jogadas -------------
    print("=== Teste de inversao de ordem de geracao de jogadas (alfa-beta) ===")
    cells = CONFIG_BOARDS[ESTADO_INVERSAO]
    turno = jogador_da_vez(cells)
    board = board_from_cells(cells)

    _, _, nos_normal, t_normal = run_repeated(AlphaBeta, board, turno, reverse=False)
    _, _, nos_invertido, t_invertido = run_repeated(AlphaBeta, board, turno, reverse=True)

    diff = nos_invertido - nos_normal
    variacao_pct = (diff / nos_normal * 100) if nos_normal else 0.0

    print(f"Estado: {ESTADO_INVERSAO}  tabuleiro: {format_board(cells)}  (vez de {turno})")
    print(f"  ordem normal    -> nos = {nos_normal:<6} tempo medio = {t_normal:.3f} ms")
    print(f"  ordem invertida -> nos = {nos_invertido:<6} tempo medio = {t_invertido:.3f} ms")
    print(f"  diferenca de nos: {diff:+d} ({variacao_pct:+.2f}%)")

    _, _, nos_mm_normal, _ = run_repeated(Minimax, board, turno, reverse=False)
    _, _, nos_mm_invertido, _ = run_repeated(Minimax, board, turno, reverse=True)
    print(f"  (minimax sem poda, para comparacao: nos normal = {nos_mm_normal}, "
          f"nos invertido = {nos_mm_invertido})")


if __name__ == "__main__":
    main()