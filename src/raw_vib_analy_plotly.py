# Plotly를 사용한 인터랙티브 그래프

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.fft import fft, fftfreq
from scipy.integrate import cumulative_trapezoid
from scipy.signal import detrend
import os

# Plotly 한글 폰트 설정
FONT_FAMILY = "Malgun Gothic"  # Windows 한글 폰트
FONT_SIZE = 13
TITLE_FONT_SIZE = 15

# 1. 데이터 로드 함수
def load_data(file_path, data_col_idx=0, has_header=True):
    """
    CSV 파일에서 진동 데이터를 로드합니다.

    Args:
        file_path (str): CSV 파일 경로
        data_col_idx (int): 진동 데이터가 있는 컬럼 인덱스 (기본 0)
        has_header (bool): CSV 파일에 헤더가 있는지 여부 (기본 True)

    Returns:
        y (numpy array): 진동 데이터 배열
        data_col_name (str): 데이터 컬럼 이름
        df (DataFrame): 전체 데이터프레임
    """
    df = pd.read_csv(file_path, header=None if not has_header else 0)
    data_col_name = df.columns[data_col_idx] if has_header else f"Column {data_col_idx}"
    y = df.iloc[:, data_col_idx].values

    return y, data_col_name, df


# 2. 시간 축 설정 함수
def setup_time_axis(df, y, time_col_idx=None, fs_input=None):
    """
    시간 축과 샘플링 레이트를 설정합니다.

    Args:
        df (DataFrame): 데이터프레임
        y (numpy array): 진동 데이터 배열
        time_col_idx (int, optional): 시간 데이터가 있는 컬럼 인덱스. 없으면 None.
        fs_input (float, optional): 시간 열이 없을 경우 수동으로 입력할 샘플링 레이트(Hz).

    Returns:
        t (numpy array): 시간 배열
        dt (float): 시간 간격 (초)
        fs (float): 샘플링 레이트 (Hz)
    """
    if time_col_idx is not None:
        t = df.iloc[:, time_col_idx].values
        dt = np.mean(np.diff(t))
        fs = 1 / dt
    else:
        if fs_input is None:
            print("오류: 시간 컬럼이 없으면 샘플링 레이트(fs_input)를 반드시 입력해야 합니다.")
            return None, None, None
        fs = fs_input
        dt = 1 / fs
        N = len(y)
        t = np.linspace(0, (N-1)*dt, N)

    print(f"분석 정보: 데이터 길이={len(y)}, 추정/입력 Fs={fs:.2f} Hz")
    return t, dt, fs


# 3. FFT 처리 함수 (주파수 도메인 변환)
def compute_fft(y, dt):
    """
    진동 데이터를 FFT로 주파수 도메인으로 변환합니다.

    Args:
        y (numpy array): 진동 데이터 배열
        dt (float): 시간 간격 (초)

    Returns:
        xf (numpy array): 주파수 배열 (Hz)
        fft_magnitude (numpy array): FFT 진폭 스펙트럼
    """
    N = len(y)
    yf = fft(y)
    xf = fftfreq(N, dt)[:N//2]

    # 진폭 스펙트럼: DC 성분은 1/N, 나머지는 2/N
    fft_magnitude = np.abs(yf[0:N//2])
    fft_magnitude[0] = fft_magnitude[0] / N  # DC 성분
    fft_magnitude[1:] = 2.0 / N * fft_magnitude[1:]  # 나머지

    return xf, fft_magnitude


# 4. 적분 처리 함수
def integrate_data(y, t):
    """
    진동 데이터를 시간 도메인에서 적분합니다.
    드리프트 방지를 위한 전처리 및 후처리 과정이 포함되었습니다.

    Args:
        y (numpy array): 진동 데이터 배열
        t (numpy array): 시간 배열

    Returns:
        y_final (numpy array): 드리프트가 보정된 적분 데이터 배열
    """
    # 1. 적분 전 평균 제거 (Pre-processing)
    # 가속도 데이터의 DC Offset(0이 아닌 평균값)을 제거하여 적분 시 발산을 방지합니다.
    y_centered = y - np.mean(y)

    # 2. 적분 수행
    y_integrated = cumulative_trapezoid(y_centered, t, initial=0)

    # 3. 적분 후 선형 경향 제거 (Post-processing)
    # 적분 과정에서 발생할 수 있는 잔여 선형 드리프트를 제거합니다.
    y_final = detrend(y_integrated)

    return y_final


# 5. 그래프 그리기 함수 (Plotly 버전)
def plot_results(t, y, xf, fft_magnitude, y_integrated, xf_integrated, fft_magnitude_integrated, data_col_name, fsize):
    """
    시간 도메인, 주파수 도메인, 적분 데이터(시간/주파수 도메인)를 Plotly 인터랙티브 그래프로 그립니다.

    Args:
        t (numpy array): 시간 배열
        y (numpy array): 원본 진동 데이터
        xf (numpy array): 주파수 배열
        fft_magnitude (numpy array): FFT 진폭 스펙트럼
        y_integrated (numpy array): 적분된 데이터 (시간 도메인)
        xf_integrated (numpy array): 적분된 데이터의 주파수 배열
        fft_magnitude_integrated (numpy array): 적분된 데이터의 FFT 진폭 스펙트럼
        data_col_name (str): 데이터 컬럼 이름
        to_save (str): 이미지 저장 경로
        fsize (tuple): 그래프 크기 (width, height)
    """

    # Plotly 레이아웃 공통 설정
    def get_layout(title, xaxis_title, yaxis_title, width=None, height=None):
        """공통 레이아웃 설정 함수"""
        layout = go.Layout(
            title=dict(
                text=title,
                font=dict(size=TITLE_FONT_SIZE, family=FONT_FAMILY)
            ),
            xaxis=dict(
                title=dict(text=xaxis_title, font=dict(size=FONT_SIZE, family=FONT_FAMILY)),
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=1
            ),
            yaxis=dict(
                title=dict(text=yaxis_title, font=dict(size=FONT_SIZE, family=FONT_FAMILY)),
                showgrid=True,
                gridcolor='lightgray',
                gridwidth=1
            ),
            font=dict(family=FONT_FAMILY, size=FONT_SIZE),
            legend=dict(font=dict(size=12, family=FONT_FAMILY)),
            template='plotly_white',
            width=width,
            height=height
        )
        return layout

    # (1) 시간 도메인 원본 데이터
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=t,
        y=y,
        mode='lines',
        name='Raw Data (Time Domain)',
        line=dict(color='blue', width=1),
        hovertemplate='Time: %{x:.4f} s<br>Amplitude: %{y:.4f}<extra></extra>'
    ))
    fig1.update_layout(get_layout(
        title=f'Time Domain: {data_col_name}',
        xaxis_title='Time (s)',
        yaxis_title='Amplitude',
        width=fsize[0]*80 if fsize else None,
        height=fsize[1]*80 if fsize else None
    ))
    fig1.show()

    # (2) FFT (주파수 도메인) - 원본 데이터
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=xf,
        y=fft_magnitude,
        mode='lines',
        name='FFT Magnitude',
        line=dict(color='red', width=1),
        hovertemplate='Frequency: %{x:.4f} Hz<br>Magnitude: %{y:.4f}<extra></extra>'
    ))
    fig2.update_layout(get_layout(
        title='Frequency Domain (FFT) - Original Data',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude',
        width=fsize[0]*80 if fsize else None,
        height=fsize[1]*80 if fsize else None
    ))
    fig2.show()

    # (3) 적분 데이터 그래프 (시간 도메인)
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=t,
        y=y_integrated,
        mode='lines',
        name='Integrated Data',
        line=dict(color='green', width=1),
        hovertemplate='Time: %{x:.4f} s<br>Integrated Amplitude: %{y:.4f}<extra></extra>'
    ))
    fig3.update_layout(get_layout(
        title='Integrated Data (Time Domain)',
        xaxis_title='Time (s)',
        yaxis_title='Integrated Amplitude',
        width=fsize[0]*80 if fsize else None,
        height=fsize[1]*80 if fsize else None
    ))
    fig3.show()

    # (4) 적분 데이터 그래프 (주파수 도메인)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=xf_integrated,
        y=fft_magnitude_integrated,
        mode='lines',
        name='FFT Magnitude (Integrated)',
        line=dict(color='purple', width=1),
        hovertemplate='Frequency: %{x:.4f} Hz<br>Magnitude: %{y:.4f}<extra></extra>'
    ))
    fig4.update_layout(get_layout(
        title='Frequency Domain (FFT) - Integrated Data',
        xaxis_title='Frequency (Hz)',
        yaxis_title='Magnitude',
        width=fsize[0]*80 if fsize else None,
        height=fsize[1]*80 if fsize else None
    ))
    fig4.show()

# Main 함수: 모든 함수를 순차적으로 실행
def analyze_vibration_data(file_path, fsize, data_col_idx=0, time_col_idx=None, fs_input=None, has_header=True):
    """
    진동 데이터를 분석하는 메인 함수입니다.
    각 기능 단위 함수를 순차적으로 호출합니다.

    Args:
        file_path (str): CSV 파일 경로
        data_col_idx (int): 진동 데이터가 있는 컬럼 인덱스 (기본 0)
        time_col_idx (int, optional): 시간 데이터가 있는 컬럼 인덱스. 없으면 None.
        fs_input (float, optional): 시간 열이 없을 경우 수동으로 입력할 샘플링 레이트(Hz).
        has_header (bool): CSV 파일에 헤더가 있는지 여부 (기본 True)
    """
    # 1. 데이터 로드
    y, data_col_name, df = load_data(file_path, data_col_idx, has_header)

    # 2. 시간 축 설정
    t, dt, fs = setup_time_axis(df, y, time_col_idx, fs_input)
    if t is None:  # 오류 발생 시 종료
        return

    # 3. FFT 처리 (원본 데이터)
    xf, fft_magnitude = compute_fft(y, dt)

    # 4. 적분 처리
    y_integrated = integrate_data(y, t)

    # 5. FFT 처리 (적분된 데이터)
    xf_integrated, fft_magnitude_integrated = compute_fft(y_integrated, dt)

    # 6. 그래프 그리기
    plot_results(t, y, xf, fft_magnitude, y_integrated, xf_integrated, fft_magnitude_integrated, data_col_name, fsize)

# 실행
file_path = r"PHM-prj\PHM_2_VibLow\프로젝트 2\과제 데이터\A_ 1조 Extruder Gear Bearing결함.csv"
fsize = (18, 8)

analyze_vibration_data(
    file_path=file_path,
    fsize=fsize,
    data_col_idx=1,        # 두 번째 컬럼(Series0)이 진동 데이터
    time_col_idx=0,        # 첫 번째 컬럼(X)이 시간 데이터
    has_header=True        # 헤더가 있음 (X, Series0)
)
