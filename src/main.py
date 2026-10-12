import flet as ft
import pandas as pd

class Interface():
    def __init__(self):
        
        self.arquivos_subidos:list[list] = []
        self.planilhas_subidas:list[list] = []
        self.arquivo_planilha_ref:list = []
        self.arquivo_planilha_comp:list = []

        self.codigos1:list = []
        self.codigos2:list = []
        self.codigos_divergentes:list = []

        self.codigos1_disciplina:list = []
        self.codigos2_disciplina:list = []

        self.txt_planilha1:str = ''
        self.txt_planilha2:str = ''

        self.lista_disciplinas:list[str] = [] # lista de disciplinas da tabela 1 

        self.df_f1 = pd.DataFrame() # dataframe da tabela 1
        self.df_f2 = pd.DataFrame() # dataframe da tabela 2

        self.sp1np2:list[list[str]] = []
        self.sp2np1:list[list[str]] = []


def main(page:ft.Page):

    # configs da página
    page.title = "Comparador de planilhas"
    page.window.resizable = False
    page.window.width = 755
    page.window.height = 700
    #page.theme_mode = ft.ThemeMode.DARK
    #page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREY)
 
    inter = Interface()
    
    # funções da página

    # quando um arquivo for selecionado

    async def arquivo_selecionado1(e:ft.Event[ft.Button]): # referência

        files = await ft.FilePicker().pick_files(allow_multiple=False)

        if len(files)>0 and type(e) != None: # se algum arquivo foi selecionado:
            ee:ft.FilePickerFile = files[0]
            if ee.name.strip().endswith(".csv"): # se a extensão do arquivo é .csv
                inter.arquivo_planilha_ref.clear()
                inter.arquivo_planilha_ref.append(ee.name) # adicionar à lista de planilhas
                inter.arquivo_planilha_ref.append(ee.path) # adicionar à lista de planilhas
                inter.arquivo_planilha_ref.append(ee.size) # adicionar à lista de planilhas
                inter.txt_planilha1 = ee.name
            else:
                    print('O arquivo selecionado não é csv')

        else: # caso nada tenha sido selecionado
            print("Nada foi selecionado")
        txt_arquivo1.value = ee.name
        page.update()    

    async def arquivo_selecionado2(e:ft.Event[ft.Button]): # referência

        files = await ft.FilePicker().pick_files(allow_multiple=False)

        if len(files)>0 and type(e) != None: # se algum arquivo foi selecionado:
            ee:ft.FilePickerFile = files[0]
            if ee.name.strip().endswith(".csv"): # se a extensão do arquivo é .csv
                inter.arquivo_planilha_comp.clear()
                inter.arquivo_planilha_comp.append(ee.name) # adicionar à lista de planilhas
                inter.arquivo_planilha_comp.append(ee.path) # adicionar à lista de planilhas
                inter.arquivo_planilha_comp.append(ee.size) # adicionar à lista de planilhas
                inter.txt_planilha2 = ee.name
            else:
                    print('O arquivo selecionado não é csv')

        else: # caso nada tenha sido selecionado
            print("Nada foi selecionado")
        txt_arquivo2.value = ee.name
        page.update()        

    def atualizar_listas_conf():

        # separando os códigos pertencentes à disciplina selecionada no dropdown
        #print(f'value: {dropdown_lista_disciplinas.value.strip()}')
        temp_tb = inter.df_f1[inter.df_f1['curso'] == dropdown_lista_disciplinas.value]
        temp_tb2 = inter.df_f2[inter.df_f2['curso'] == dropdown_lista_disciplinas.value]
        inter.codigos1 = temp_tb['codigo'].to_list()
        inter.codigos2 = temp_tb2['codigo'].to_list()
        inter.codigos1.sort()
        inter.codigos2.sort()

        # adicionando os códigos separados aao listview
        listView_plan1.controls.clear()
        listView_plan2.controls.clear()
        listView_plan_na.controls.clear()

        # buscando na sala os códigos subidos
        for x in range(0,len(inter.codigos1)):
            
            if inter.codigos1[x] not in inter.codigos2: # codigos da plan1 na plan2
                listView_plan1.controls.append(ft.Row([ft.Text(f'{x+1} | {inter.codigos1[x]}',color=ft.Colors.RED)]))
                listView_plan_na.controls.append(ft.Row([ft.Text(f'({x+1}) {inter.codigos1[x]} | Planilha 1')]))
                inter.codigos_divergentes.append(f'({x+1}) {inter.codigos1[x]} | Planilha 1')
            else:
                listView_plan1.controls.append(ft.Row([ft.Text(f'{x+1} | {inter.codigos1[x]}')]))

        # buscando no csv os alunos na sala
        for x in range(0,len(inter.codigos2)):
            if inter.codigos2[x] not in inter.codigos1: # codigos da plan1 na plan2
                listView_plan2.controls.append(ft.Row([ft.Text(f'{x+1} | {inter.codigos2[x]}',color=ft.Colors.RED)]))
                listView_plan_na.controls.append(ft.Row([ft.Text(f'({x+1}) {inter.codigos2[x]} | Planilha 2')]))
                inter.codigos_divergentes.append(f'({x+1}) {inter.codigos2[x]} | Planilha 2')
            else:
                listView_plan2.controls.append(ft.Row([ft.Text(f'{x+1} | {inter.codigos2[x]}')]))
        
        page.update()

    def iniciar_comparacao_interface(e):
    
        # converter planilhas para dataframe
        df1:pd.DataFrame = pd.read_csv(str(inter.arquivo_planilha_ref[1]),sep=';',encoding="latin_1")
        df2:pd.DataFrame = pd.read_csv(str(inter.arquivo_planilha_comp[1]),sep=';',encoding="latin_1")

        # separando colunas que serão trabalhadas (username, firstname, course1)
        inter.df_f1['codigo'] = df1['username']
        #inter.df_f1['nome'] = df1['firstname']
        inter.df_f1['curso'] = df1['course1']

        inter.df_f2['codigo'] = df2['username']
        #inter.df_f2['nome'] = df2['firstname']
        inter.df_f2['curso'] = df2['course1']

        # separando as disciplinas dos cursos de pós
        coiso2 = inter.df_f1.groupby('curso').sample(1)
        coiso2 = coiso2['curso']
        inter.lista_disciplinas = coiso2.to_list() # interface

        # outros
        print(inter.lista_disciplinas)
        listView_plan1.controls.clear()
        listView_plan2.controls.clear()
        listView_plan_na.controls.clear()
        dropdown_att_opcoes(dropdown_lista_disciplinas,inter.lista_disciplinas)
        page.update()

    def dropdown_att_opcoes(dropdown:ft.Dropdown,opcoes:list):
        dropdown.options.clear()
        for opcao in opcoes:
            dropdown.options.append(ft.DropdownOption(text=opcao))
        page.update()

    def dropdown_changed(e):
        #print(f'e: {e}')
        #atualizar_lista(listView_plan1, inter.df_f1)
        #atualizar_lista(listView_plan2, inter.df_f2)
        #atualizar_lista_na(listView_plan_na,[listView_plan1,listView_plan2],inter.df_f1,inter.df_f2)
        atualizar_listas_conf()
        
        page.update()

    def printar_codigos_divergentes(e):
        print('=='* 20)
        for codigo in inter.codigos_divergentes:
            print(codigo)

    # criando layout da página

    # área de arquivos
    btn_comparar_arquivos= ft.Button('COMPARAR', on_click=iniciar_comparacao_interface)
    btn_subir_arquivo1= ft.IconButton(ft.Icons.FILE_UPLOAD, on_click=arquivo_selecionado1)
    btn_subir_arquivo2= ft.IconButton(ft.Icons.FILE_UPLOAD, on_click=arquivo_selecionado2)
    btn_printar_divergencia= ft.Button('PRINT', on_click=printar_codigos_divergentes)


    txt_arquivo1 = ft.Text('')
    txt_arquivo2 = ft.Text('')


    container_arquivos = ft.Container(
        bgcolor=ft.Colors.GREY_400,
        padding=10,
        margin=10,
        border_radius=5,
        content=ft.Column(
            [
                #ft.Row([filePicker,filePicker1,filePicker2]),
                ft.Row([ft.Text("Arquivos para comparação:")]),
                ft.Row([btn_subir_arquivo1,ft.Text(f"Planilha 1: "),txt_arquivo1]),
                ft.Row([btn_subir_arquivo2,ft.Text(f"planilha 2: "),txt_arquivo2]),
                ft.Row([btn_comparar_arquivos])
            ]
        )
    )


    # área de comparação

    listView_plan1 = ft.ListView()
    listView_plan2 = ft.ListView()
    listView_plan_na = ft.ListView()


    listView_plan1.controls.append(ft.Row([ft.Text('linha 1')]))
    listView_plan2.controls.append(ft.Row([ft.Text('linha 2')]))
    listView_plan_na.controls.append(ft.Row([ft.Text('linha 3')]))


    dropdown_lista_disciplinas = ft.Dropdown(
        width=500,
        editable=True,
        label="Disciplina",
        enable_filter=True,
        options=inter.lista_disciplinas,
        on_text_change=dropdown_changed
        
    )


    container_comparacao = ft.Container(
        bgcolor=ft.Colors.GREY_400,
        padding=10,
        margin=10,
        border_radius=5,
        
        content=ft.Column([
            ft.Row([
                dropdown_lista_disciplinas
            ]),
            ft.Row(
                [
                    ft.Container(
                    bgcolor=ft.Colors.GREY_300,
                    padding=10,
                    margin=10,
                    border_radius=5,
                    width=150,
                    height=300,
                    content=ft.Column([ft.Row([ft.Text('Planilha 1')]),ft.Column([listView_plan1],expand=1,wrap=False, scroll=ft.ScrollMode.ALWAYS)])
                    ),
                    ft.Container(
                    bgcolor=ft.Colors.GREY_300,
                    padding=10,
                    margin=10,
                    border_radius=5,
                    width=150,
                    height=300,
                    content=ft.Column([ft.Row([ft.Text('Planilha 2')]),ft.Column([listView_plan2],expand=1,wrap=False, scroll=ft.ScrollMode.ALWAYS)])
                    ),
                    ft.Container(
                    bgcolor=ft.Colors.GREY_300,
                    padding=10,
                    margin=10,
                    border_radius=5,
                    width=300,
                    height=300,
                    content=ft.Column([
                        ft.Row([ft.Text('códigos Divergentes')]),
                        ft.Column([listView_plan_na],expand=1,wrap=False, scroll=ft.ScrollMode.ALWAYS),
                        ft.Row([btn_printar_divergencia])
                        ]),
                        
                    )
                ]
            )
        ])
    )

    layout =ft.Column([container_arquivos,container_comparacao])

    page.add(layout)
    page.update()


ft.run(main)

    