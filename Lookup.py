from numpy import var
import streamlit as st
import pandas as pd
import random

def process_excel_file(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    
    # Gom các cột cùng ngày vào cùng một hàng và chuyển đổi giá trị thành chuỗi
    grouped_data = df.groupby(['connectdata1'])['Điểm bán'].agg(lambda x: ','.join(str(x) for x in x)).reset_index()

    # Kiểm tra sự trùng lặp và liền kề
    grouped_data['Trùng lặp'] = grouped_data.duplicated(subset='Điểm bán', keep=False)
    grouped_data['Liền kề'] = grouped_data['Điểm bán'] == grouped_data['Điểm bán'].shift()

    # Lọc ra các ngày có điểm bán trùng lặp và liền kề
    days_with_consecutive_duplicate_sales = grouped_data.loc[grouped_data['Trùng lặp'] & grouped_data['Liền kề'], 'connectdata1'].unique()

    # Trả về kết quả xử lý
    return days_with_consecutive_duplicate_sales

# Giao diện người dùng
st.title("Ứng dụng xử lý tệp Excel")

# Hiển thị thành phần giao diện để người dùng tải lên tệp
uploaded_file = st.file_uploader("Chọn tệp Excel", type=["xlsx"])
if uploaded_file:
    # Đọc tệp Excel và lưu dữ liệu vào biến df
    df = pd.read_excel(uploaded_file)
    
    # Xử lý tệp Excel nếu người dùng đã tải lên
    days_with_consecutive_duplicate_sales = process_excel_file(df)
    
    # Hiển thị kết quả xử lý
    if len(days_with_consecutive_duplicate_sales) > 0:
        st.write("Ngày có điểm bán trùng lặp và liền kề:")
        
        # Tạo một khung HTML để hiển thị dữ liệu
        html_table = "<table class='custom-table'>"
        html_table += "<tr><th>Tên - Ngày - Điểm bán thứ</th><th>Điểm bán (nan là không có)</th></tr>"
        
        # Lưu trữ màu ngẫu nhiên cho mỗi nhóm dữ liệu trùng lặp và liền kề
        color_map = {}
        
        for day in days_with_consecutive_duplicate_sales:
            # Lọc dữ liệu có cùng ngày
            filtered_data = df[df['connectdata1'] == day]['Điểm bán'].values
            # Tạo hàng cho dữ liệu trong khung HTML
            for i, value in enumerate(filtered_data):
                
                html_table += f"<tr class='{day}'><td>{day}</td><td>{value}</td></tr>"
        
        html_table += "</table>"
        
        # CSS để tô màu bảng và tùy chỉnh kiểu dáng nút tô màu
        css = """
        <style>
            /* CSS cho bảng */
            .custom-table {
                border-collapse: collapse;
                width: 100%;
            }
            .custom-table th,
            .custom-table td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            .custom-table tr:hover {
                background-color: #f5f5f5;
            }
            .custom-table tr.active {
                background-color: #ffcc00;
            }
            .custom-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            
        </style>
        """
        
        # Mã JavaScript để tô màu các nhóm dữ liệu trùng lặp và liền kề
        js = """
        <script>
            const rows = document.querySelectorAll('.custom-table tr');
            let currentColor = '';

            rows.forEach((row) => {
                const cells = row.getElementsByTagName('td');
                const day = cells[0].textContent;

                if (day !== '') {
                    if (currentColor === '') {
                        currentColor = row.style.backgroundColor;
                    } else if (currentColor !== row.style.backgroundColor) {
                        currentColor = row.style.backgroundColor;
                    }

                    if (currentColor !== '') {
                        row.style.backgroundColor = currentColor;
                    }
                }
            });
        </script>
        """
        
        # Hiển thị khung HTML, CSS và JavaScript
        st.markdown(css + html_table + js, unsafe_allow_html=True)
    else:
        st.write("Không có ngày nào có điểm bán trùng lặp và liền kề trong tệp Excel.")