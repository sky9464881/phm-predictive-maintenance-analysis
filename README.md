# 진동 데이터 기반 PHM 예지보전 분석
> FFT와 Envelope Analysis를 기반으로 회전체 설비의 진동 데이터를 해석하고, 베어링·기어·팬의 이상 징후를 진단한 프로젝트

<img width="806" height="656" alt="freq resolution 1Hz, raw" src="https://github.com/user-attachments/assets/fac16438-3fdf-4502-ae5e-62785dab6935" />

> 최종 결과에 관한 자세한 내용은 results/reports/3조_PHM_최종발표본 에서 확인 가능합니다
## Overview
본 프로젝트는 회전체 설비에서 수집한 진동 데이터를 분석해 설비의 이상 징후를 조기에 파악하고, 고장 원인을 진단하기 위해 수행한 PHM(Predictive Health Management) 프로젝트입니다.

단순히 정상/비정상을 구분하는 수준을 넘어, FFT 스펙트럼과 포락선 분석을 통해 회전 주파수(1X), 하모닉, GMF, BPFO/BPFI/BSF/FTF, Sideband 성분을 해석하고 실제 설비 점검 방향까지 연결하는 것을 목표로 했습니다.

특히 Fan, 모터 세트, 베어링 외륜 결함 의심 데이터를 대상으로 주파수 패턴 변화를 비교하여 설비 이상 상태를 진단하고, 각 설비별 보전 방향을 도출했습니다.

---

## Project Goals
- 진동 데이터 기반 설비 건전성 예측 및 이상 징후 조기 탐지
- FFT 및 Envelope Analysis를 활용한 주파수 성분 해석
- 베어링, 기어, 팬 설비의 고장 원인 추정
- 진단 결과를 실제 점검 및 유지보수 방향과 연결

---

## Tech Stack
- **Language**
  - Python

- **Analysis / Signal Processing**
  - FFT
  - Envelope Analysis
  - Hilbert Transform
  - Window Function
  - Spectrogram
  - Waterfall

- **Domain Knowledge**
  - Bearing Fault Frequency Analysis
  - GMF(Gear Mesh Frequency) Analysis
  - Sideband Analysis
  - Harmonics Analysis

- **Environment**
  - 가속도 센싱 데이터 기반 진동 분석 환경
  - 약 1초 길이의 비실시간 진동 데이터 사용

---

## Key Tasks
- 가속도 기반 진동 데이터의 Time Domain / FFT 스펙트럼 분석
- 샘플링 주파수, 주파수 범위, 분해능, Window Size 등 분석 파라미터 정의
- Hilbert Transform 기반 Envelope Analysis 수행
- Fan 1/2/3단 정상·비정상 데이터 비교 분석
- 모터 세트별 1X, GMF, BPFO/BPFI/BSF/FTF, Sideband 성분 해석
- 분석 결과를 바탕으로 정렬 불량, 헐거움, 베어링 외륜 손상, 기어 치 손상, 마찰(Rubbing) 등 이상 원인 진단
- 진단 결과에 따른 유지보수 및 점검 방향 제안

---

## Analysis Process

### 1. 문제 정의 및 데이터 이해
베어링 외륜 결함이 의심되는 상황을 가정하고, 가속도 센싱 데이터의 시간 영역 그래프와 FFT Plot을 기반으로 초기 이상 징후를 확인했습니다.

### 2. 신호 처리 파라미터 설계
샘플링 주파수, Nyquist-Shannon 이론 기반 주파수 범위, 최대 분해능을 계산하고, 사용자 정의 최대 주파수와 분해능을 반영해 Window Size를 설정했습니다.

### 3. 신호 분석 기법 적용
기본 FFT 분석 외에도 Window Function, Envelope(Hilbert Transform 기반) 계산, 속도/변위 적분 스펙트럼 분석을 수행해 다양한 관점에서 진동 특성을 해석했습니다.

### 4. 설비별 이상 패턴 해석
Fan, 모터 세트, 베어링 결함 데이터를 대상으로 정상/비정상 스펙트럼을 비교하고, 1X, 하모닉, GMF, BPFO 계열, Sideband 간격 등을 근거로 이상 원인을 추정했습니다.

### 5. 진단 및 보전 방향 도출
분석 결과를 바탕으로 설비별 점검 포인트와 유지보수 방향을 정리하고, 추가적으로 Spectrogram / Waterfall 기반 실시간 트렌드 분석 가능성도 검토했습니다.

---

## Major Findings

### 1. 베어링 외륜 결함 의심 데이터 분석

<img width="761" height="463" alt="image" src="https://github.com/user-attachments/assets/e1497be7-055d-49f9-8a3e-aa3978826931" />


고주파 대역에서 2915 Hz 부근 최대 피크가 관측되었고, 양 옆으로 약 133 Hz 간격의 등간격 Peak가 나타났습니다. 저주파 대역에서도 133 Hz 배수 성분이 확인되어, 특정 베어링 결함 주파수 성분과의 연관성을 중심으로 추가 분석을 진행했습니다.

또한 Envelope 및 속도 적분 스펙트럼을 함께 비교하면서, 단순 FFT만으로는 보기 어려운 결함 관련 주기 성분을 보완적으로 해석했습니다.

### 2. Fan 이상 진단

<img width="749" height="468" alt="image" src="https://github.com/user-attachments/assets/2097d506-a2cc-44ca-a079-1d81d1cdffab" />


Fan은 정상 대비 비정상 상태에서 각 단수별 총진동이 크게 증가했습니다.

- 1단: 0.35 → 2.32 mm/s rms
- 2단: 0.43 → 3.07 mm/s rms
- 3단: 0.85 → 5.67 mm/s rms

비정상 상태에서는 1X 피크값이 지배적으로 증가했고, 단수가 올라갈수록 하모닉 성분도 함께 증폭되는 양상이 나타났습니다. 이를 통해 선풍기 날개의 **불균형 및 편심** 가능성을 진단했으며, 즉각적인 밸런싱 작업 또는 날개 교체 필요성을 도출했습니다.


## 모터 세트
<img width="710" height="365" alt="image" src="https://github.com/user-attachments/assets/27196e49-b0d0-4c7e-9949-752292b38642" />


### 3. 모터 세트 1 - 베벨 기어 진단
정방향 구동에서는 3축 GMF(36.3 Hz)와 조화 성분이 두드러지게 나타났고, 역방향에서는 GMF보다 1X 증가가 더 뚜렷하게 관측되었습니다.

또한 36.3 Hz 주변에서 1.8 Hz 간격의 Sideband가 확인되어 특정 축 회전 주파수와의 연관성을 분석했고, 최종적으로 **축 정렬 불량과 편심** 가능성을 진단했습니다.

### 4. 모터 세트 1 - 2번 모터 진단
1X의 분수 조화 성분(1/2X)이 뚜렷하게 나타났고, BPFO(약 72.8 Hz) 중심의 조화 성분도 함께 검출되었습니다.

이를 바탕으로 다음 두 가지 가능성을 도출했습니다.

- **기계적 헐거움**
- **베어링 외륜 손상**

권장 조치로는 베어링 교체 및 체결 상태 점검/수리를 제안했습니다.


### 5. 모터 세트 2 - 1번 모터 진단
72 Hz 부근 GMF 및 조화 성분을 중심으로 분석한 결과, 분수 조화 성분과 Sideband가 관찰되었습니다. 특히 약 1.6 Hz 간격의 Sideband를 통해 특정 축 기어의 느슨함 또는 손상 가능성을 추정했습니다.

### 6. 모터 세트 2 - 2번 모터 진단
정상 대비 비정상 데이터에서 고주파 영역 신호가 크게 증가했고, Envelope 분석에서도 93.2 Hz 조화 성분 증가가 확인되었습니다.

이를 통해 **Rubbing(마찰)** 가능성을 진단했으며, 윤활 상태 및 2단·3단 기어단 점검 필요성을 제안했습니다.

### 7. 모터 세트 2 - 3번 모터 진단
1차 GMF(292.5 Hz) 부근 변화와 함께 약 29.59 Hz 간격의 Sideband가 확인되었습니다. 해당 간격이 1기어 회전 주파수와 유사하다는 점을 바탕으로 **기어 이빨 손상 가능성**을 도출했습니다.

---

## Results
- FFT와 Envelope Analysis를 통해 설비별 주요 이상 패턴을 주파수 성분 관점에서 해석
- Fan, 베벨 기어, 모터 세트에서 각각 불균형/편심, 정렬 불량, 헐거움, 베어링 외륜 손상, 마찰, 기어 치 손상 가능성 도출
- 단순 이상 탐지를 넘어 실제 유지보수 방향까지 연결하는 PHM 분석 흐름 경험
- 제한된 시간 안에 데이터 해석, 진단, 발표 자료 제작까지 완료

---

## What I Learned
- 진동 데이터 해석은 단순 피크 비교보다, 1X / Harmonics / GMF / Bearing Fault Frequency / Sideband를 함께 봐야 더 정확한 진단이 가능하다는 점을 배웠습니다.
- 동일 설비라도 회전 방향, 부하 조건, 고주파 대역 변화에 따라 진단 포인트가 달라질 수 있음을 확인했습니다.
- 실제 설비 데이터를 다룰 때는 신호처리 이론뿐 아니라, 베어링·기어·정렬 상태에 대한 기계적 해석이 함께 필요하다는 점을 체감했습니다.

---

## Limitations
- 분석 기간이 짧아 모든 주파수 성분을 충분히 세부적으로 검토하지는 못했습니다.
- 데이터가 약 1초 길이의 비실시간 진동 패턴 중심이어서, 장기 트렌드 기반 분석에는 한계가 있었습니다.
- 일부 Sideband 구간은 분해능 한계로 인해 보다 정밀한 추가 분석이 필요했습니다.

---

## Future Improvements
- 실시간 진동 데이터 수집 및 장기 트렌드 분석 환경 구축
- Spectrogram / Waterfall 기반 시간-주파수 변화 분석 강화
- 설비 상태 분류를 위한 머신러닝/딥러닝 기반 진단 구조 확장
- 센서 설치 위치, 샘플링 조건, 분해능 최적화를 통한 분석 정확도 개선

---
