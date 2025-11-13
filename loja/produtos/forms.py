from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, IntegerField, StringField, BooleanField, TextAreaField, validators, FloatField, SubmitField


class Addprodutos(Form):
    nome = StringField('Nome :',[validators.DataRequired()])
    sexo = StringField('Sexo :',[validators.DataRequired()])
    idade = IntegerField('Idade :',[validators.DataRequired()])
    porte = StringField('Porte :',[validators.DataRequired()])
    comportamento = StringField('Comportamento :',[validators.DataRequired()])
    compatibilidade = StringField('Compatibilidade :',[validators.DataRequired()])
    historico_resgate = TextAreaField('Histórico de Resgate :',[validators.DataRequired()])
    local_do_abrigo = StringField('Local do Abrigo :',[validators.DataRequired()])
    data_entrada = StringField('Data de Entrada :',[validators.DataRequired()])
    status = StringField('Status :',[validators.DataRequired()])
    data_adocao = StringField('Data de Adoção :',[validators.DataRequired()])
    data_falecimento = StringField('Data de Falecimento :',[validators.DataRequired()])
    descricao = StringField('Observação :',[validators.DataRequired()])
    
    preco = FloatField('Preço :',[validators.DataRequired()])
    desconto = IntegerField('Desconto :',[validators.DataRequired()])
    estoque = IntegerField('Estoque :',[validators.DataRequired()])
    cor = TextAreaField('Cor :',[validators.DataRequired()])
    



    
    imagem_1 = FileField('Imagem 1 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_2 = FileField('Imagem 2 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
    imagem_3 = FileField('Imagem 3 :', validators=[FileAllowed(['jpg','png','gif','jpeg','bmp'])])
