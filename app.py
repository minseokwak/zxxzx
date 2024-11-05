import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 파일 업로드 인터페이스
uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])

# 파일이 업로드되었는지 확인
if uploaded_file is not None:
    # 엑셀 파일의 15번째 행부터 A, H, I 열만 읽기
    data = pd.read_excel(uploaded_file, skiprows=14, usecols="A,H,I", names=["Component ID", "Quantity", "Unit"])

    # 데이터가 제대로 로드됐는지 확인
    st.write("데이터 미리보기:")
    st.dataframe(data.head())

    # 데이터에 'Component ID', 'Quantity', 'Unit' 컬럼이 있는지 확인
    if 'Component ID' in data.columns and 'Quantity' in data.columns and 'Unit' in data.columns:
        # 특정 Component ID만 필터링
        selected_components = [
            'Cast-In-Place Concrete', 'Steel Structure', 'Glass', 
            'Wood', 'Plasterboard', 'Plastic'
        ]
        filtered_data = data[data['Component ID'].isin(selected_components)].copy()

        # Quantity와 Unit을 결합하여 새로운 컬럼 생성
        filtered_data['Quantity with Unit'] = filtered_data['Quantity'].astype(str) + ' ' + filtered_data['Unit']

        # 막대그래프 생성 (Matplotlib)
        st.write("## 자재별 수량 - 막대그래프")
        plt.figure(figsize=(10, 6))
        plt.bar(filtered_data['Component ID'], filtered_data['Quantity'], color='skyblue')
        plt.xlabel("Component ID")
        plt.ylabel("Quantity")
        plt.title("Quantity by Component ID")
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # 자재별 수량에 대한 파이 차트 생성 (Plotly)
        st.write("## 자재별 수량 - 파이 차트")
        fig_quantity = px.pie(filtered_data, values='Quantity', names='Component ID', 
                               title="Quantity Distribution by Component ID",
                               hover_data={'Quantity with Unit': True})
        fig_quantity.update_traces(textinfo='label+percent', hovertemplate='Component ID: %{label}<br>Quantity: %{customdata[0]}')
        st.plotly_chart(fig_quantity)

        # 재활용 가능 여부 추가
        recycling_dict = {
            'Cast-In-Place Concrete': '가능',
            'Cement Brick': '가능',
            'Steel Structure': '가능',
            'Glass': '가능',
            'Wood': '가능',
            'Plasterboard': '불가능',
            'Plastic': '불가능'
        }

        # 재활용 가능 여부를 기반으로 새로운 열 추가
        filtered_data.loc[:, 'Recyclable'] = filtered_data['Component ID'].map(recycling_dict)

        # 재활용 가능성과 불가능성을 기반으로 그룹화
        recycling_summary = filtered_data.groupby('Recyclable')['Quantity'].sum().reset_index()

        # 재활용 가능성에 따른 파이 차트 생성 (Plotly)
        st.write("## 재활용 가능성 - 파이 차트")
        fig_recycling = px.pie(recycling_summary, values='Quantity', names='Recyclable', 
                                title="Recycling Possibility Distribution",
                                hover_data={'Quantity': True})
        fig_recycling.update_traces(textinfo='label+percent', hovertemplate='Recyclable: %{label}<br>Quantity: %{value}')
        st.plotly_chart(fig_recycling)

    else:
        st.error("업로드한 파일에 'Component ID', 'Quantity', 및 'Unit' 컬럼이 없습니다.")
else:
    st.info("엑셀 파일을 업로드하면 자재별 수량 그래프가 표시됩니다.")
