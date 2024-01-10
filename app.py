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

def create_msapp(dict_data):
    result = ''
    for i,record in enumerate(dict_data):
        
        result += f'''
            "'{record['column_name']}_DataCard' As typedDataCard.textualEditCard":
                BorderColor: =RGBA(245, 245, 245, 1)
                BorderStyle: =BorderStyle.Solid
                DataField: ="{record['column_name']}"
                Default: =ThisItem.'{record['column_name']}'
                DisplayMode: =Parent.DisplayMode
                DisplayName: ="{record['display_name']}"
                Fill: =RGBA(0, 0, 0, 0)
                Height: =50
                MaxLength: = 999
                Required: =false
                Update: =lbl_{record['column_name']}.Text
                Width: =683
                X: =1
                Y: =1
                ZIndex: =2

                lbl_{record['column_name']}_title As label:
                    AutoHeight: =true
                    BorderColor: =RGBA(0, 0, 0, 0)
                    BorderStyle: =BorderStyle.None
                    BorderThickness: =2
                    Color: =RGBA(50, 49, 48, 1)
                    DisabledBorderColor: =RGBA(0, 0, 0, 0)
                    DisabledColor: =RGBA(161, 159, 157, 1)
                    FocusedBorderThickness: =4
                    Font: =Font.'Segoe UI'
                    FontWeight: =FontWeight.Semibold
                    Height: =34
                    PaddingLeft: =0
                    Size: =20
                    Text: =Parent.DisplayName
                    Width: =Parent.Width - 60
                    Wrap: =false
                    X: =60
                    Y: =10
                    ZIndex: =1

                lbl_{record['column_name']} As text:
                    BorderColor: =If(IsBlank(Parent.Error), Parent.BorderColor, Color.Red)
                    BorderThickness: =2
                    Color: =RGBA(50, 49, 48, 1)
                    Default: =Parent.Default
                    DelayOutput: =true
                    DisabledBorderColor: =RGBA(0, 0, 0, 0)
                    DisabledColor: =RGBA(161, 159, 157, 1)
                    DisabledFill: =RGBA(242, 242, 241, 0)
                    DisplayMode: =Parent.DisplayMode
                    FocusedBorderThickness: =4
                    Font: =Font.'Segoe UI'
                    HoverBorderColor: =RGBA(16, 110, 190, 1)
                    HoverColor: =RGBA(50, 49, 48, 1)
                    HoverFill: =RGBA(255, 255, 255, 1)
                    MaxLength: =Parent.MaxLength
                    PaddingLeft: =5
                    PressedBorderColor: =RGBA(0, 120, 212, 1)
                    PressedColor: =RGBA(50, 49, 48, 1)
                    PressedFill: =RGBA(255, 255, 255, 1)
                    RadiusBottomLeft: =0
                    RadiusBottomRight: =0
                    RadiusTopLeft: =0
                    RadiusTopRight: =0
                    Size: =13
                    Tooltip: =Parent.DisplayName
                    Width: =Parent.Width - 60
                    X: =30
                    Y: =DataCardKey14.Y + DataCardKey14.Height + 5
                    ZIndex: =2

    '''
    return result

if data:
    df = pd.read_csv(data)
    dict_data = df.to_dict(orient='records')
    
    sql_script = create_sql_table(dict_data)
    st.write('---')
    st.code(sql_script, language="sql", line_numbers=True)
    
    excel_file = create_xls(dict_data)
    st.write('---')
    st.download_button(
        label="Download Excel worksheets",
        data=excel_file,
        file_name="file.xlsx",
        mime="application/vnd.ms-excel"
    )

    st.write('---')
    msapp = create_msapp(dict_data)
    st.code(msapp, language="yaml", line_numbers=True)

