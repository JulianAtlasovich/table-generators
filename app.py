import streamlit as st
import pandas as pd
import io

buffer = io.BytesIO()


def create_sql_table(dict_data):
    result = 'CREATE TABLE public.table_name (\n'
    result += '\tid INT GENERATED ALWAYS AS IDENTITY,\n'

    for record in dict_data:
        result += '\t' + record['column_name'] + ' ' + record['data_type'] + ' NULL,\n'

    result += 'CONSTRAINT table_name_pk PRIMARY KEY (id)\n'
    result += ');'
    return result

def create_xls(dict_data):
    columns = []
    for record in dict_data:
        columns.append(record['column_name'])

    df = pd.DataFrame(columns=columns)    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1',index=False)
    return buffer

st.title("Table Generator")
data = st.file_uploader("Upload a CSV file with columns 'column_name','display_name','input_type' and 'data_type'", type=["csv"])


if data:
    df = pd.read_csv(data)
    dict_data = df.to_dict(orient='records')
    
    sql_script = create_sql_table(dict_data)
    st.code(sql_script, language="sql", line_numbers=True)
    
    excel_file = create_xls(dict_data)
    st.download_button(
        label="Download Excel worksheets",
        data=excel_file,
        file_name="file.xlsx",
        mime="application/vnd.ms-excel"
    )

