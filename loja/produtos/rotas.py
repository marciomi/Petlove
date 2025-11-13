from flask import redirect, render_template, url_for, flash, request, session, current_app
from .forms import Addprodutos
from loja import db, app, photos
from .models import Modelo, Tema, Addproduto
import secrets, os
from flask_uploads import UploadNotAllowed
from datetime import datetime

def modelos():
    modelos = modelos = Modelo.query.join(Addproduto,(Modelo.id == Addproduto.modelo_id)).all()
    return modelos

def temas():
    temas = Tema.query.join(Addproduto,(Tema.id == Addproduto.tema_id)).all()
    return temas

@app.route('/')
def home():
    pagina = request.args.get('pagina',1, type=int)
    produtos = Addproduto.query.filter(Addproduto.estoque >0).order_by(Addproduto.id.desc()).paginate(page=pagina,per_page=4)    
    return render_template('produtos/index.html', title='Pedcaneca - Canecas Personalizadas', produtos=produtos, modelos=modelos(), temas=temas())

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method =='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.nome.like(search)).all()
        return render_template('pesquisar.html', produtos=produtos, modelos=modelos(), temas=temas())
    else:
        return redirect('/')

@app.route('/modelo/<int:id>')
def get_modelo(id):
    pagina = request.args.get('pagina',1, type=int)
    get_modelo = Modelo.query.filter_by(id=id).first_or_404()
    modelo = Addproduto.query.filter_by(modelo=get_modelo).paginate(page=pagina,per_page=4)
    return render_template('produtos/index.html', title='Pedcaneca - Canecas Personalizadas', modelo=modelo, modelos=modelos(), temas=temas(), get_modelo=get_modelo)

@app.route('/produto/<int:id>')
def pagina_unica(id):
    produto = Addproduto.query.get_or_404(id)
    return render_template('produtos/pagina_unica.html', title='Pedcaneca - Canecas Personalizadas', produto=produto, modelos=modelos(), temas=temas())

@app.route('/temas/<int:id>')
def get_tema(id):
    pagina = request.args.get('pagina',1, type=int)
    get_tema = Tema.query.filter_by(id=id).first_or_404()
    get_tema_prod = Addproduto.query.filter_by(tema=get_tema).paginate(page=pagina,per_page=4)
    return render_template('produtos/index.html', title='Pedcaneca - Canecas Personalizadas', get_tema_prod=get_tema_prod, temas=temas(), modelos=modelos(), get_tema=get_tema)

@app.route('/addmodelo', methods=['GET','POST'])
def addmodelo():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    
    if request.method=="POST":
        getmodelo = request.form.get('modelo')
        modelo = Modelo(name=getmodelo)
        db.session.add(modelo)
        flash(f'O modelo {getmodelo} cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addmodelo'))
    return render_template('/produtos/addmodelo.html', title='Cadastrar Modelos', modelo='modelo')

@app.route('/addtema', methods=['GET','POST'])
def addtema():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    
    if request.method=="POST":
        getmodelo = request.form.get('tema')
        tema = Tema(name=getmodelo)
        db.session.add(tema)
        flash(f'O Tema {getmodelo} cadastrada com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('addtema'))
    return render_template('/produtos/addmodelo.html',title='Cadastrar Temas')

@app.route('/addproduto', methods=['GET','POST'])
def addproduto():
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    modelos = Modelo.query.all()
    temas = Tema.query.all()
    form = Addprodutos(request.form)
    if request.method=="POST":
        nome = form.nome.data
        sexo = form.sexo.data
        idade = form.idade.data
        porte = form.porte.data
        comportamento = form.comportamento.data
        compatibilidade = form.compatibilidade.data
        historico_resgate = form.historico_resgate.data
        local_do_abrigo = form.local_do_abrigo.data

        str_data_entrada = request.form.get('data_entrada')
        if str_data_entrada:
            data_entrada = datetime.strptime(str_data_entrada, '%d/%m/%y').date()
        else:
            data_entrada = None  

        status = form.status.data

        str_data_adocao = request.form.get('data_adocao')
        if str_data_adocao:
            data_adocao = datetime.strptime(str_data_adocao, '%d/%m/%y').date()
        else:
            data_adocao = None

        str_data_falecimento = request.form.get('data_falecimento')
        if str_data_falecimento:
            data_falecimento = datetime.strptime(str_data_falecimento, '%d/%m/%y').date()
        else:
            data_falecimento = None

        descricao = form.descricao.data
        preco = form.preco.data
        desconto = form.desconto.data
        estoque = form.estoque.data
        cor = form.cor.data
        modelo = request.form.get('modelo')
        tema = request.form.get('tema')
        
        imagem_1 = ''
        imagem_1_file = request.files.get('imagem_1')
        if imagem_1_file and imagem_1_file.filename != '':
            try:
                imagem_1 = photos.save(imagem_1_file, name=secrets.token_hex(10) + '.')
            except UploadNotAllowed:
                imagem_1 = ''
        
        imagem_2 = ''
        imagem_2_file = request.files.get('imagem_2')
        if imagem_2_file and imagem_2_file.filename != '':
            try:
                imagem_2 = photos.save(imagem_2_file, name=secrets.token_hex(10) + '.')
            except UploadNotAllowed:
                imagem_2 = ''
        else:
            imagem_2 = ''
       
        imagem_3 = ''
        imagem_3_file = request.files.get('imagem_3')
        if imagem_3_file and imagem_3_file.filename != '':
            try:
                imagem_3 = photos.save(imagem_3_file, name=secrets.token_hex(10) + '.')
            except UploadNotAllowed:
                imagem_3 = ''
        else:
            imagem_3 = ''

        addpro = Addproduto(data_adocao=data_adocao, data_falecimento=data_falecimento, data_entrada=data_entrada, local_do_abrigo=local_do_abrigo, status=status, sexo=sexo, idade=idade, porte=porte, comportamento=comportamento, compatibilidade=compatibilidade, historico_resgate=historico_resgate,   nome=nome, preco=preco, desconto=desconto, estoque=estoque, cor=cor, descricao=descricao, modelo_id=modelo, tema_id=tema, imagem_1=imagem_1, imagem_2=imagem_2, imagem_3=imagem_3)
        db.session.add(addpro)
        flash(f'Produto {nome} foi cadastrado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('admin')) 
    return render_template('produtos/addproduto.html', title="Cadastrar Produtos",form=form, modelos=modelos, temas=temas)

@app.route('/atualizarmodelo/<int:id>', methods=['GET','POST'])
def atualizarmodelo(id):
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    atualizarmodelo = Modelo.query.get_or_404(id)
    modelo = request.form.get('modelo')
    if request.method=='POST':
        atualizarmodelo.name = modelo
        flash(f'O modelo foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('modelo'))
    return render_template('/produtos/atualizarmodelo.html', title='Atualizar Modelos', atualizarmodelo=atualizarmodelo)

@app.route('/deletemodelo/<int:id>', methods=['GET','POST'])
def deletemodelo(id):
    modelo = Modelo.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(modelo)
        db.session.commit()
        flash(f'O modelo {modelo.name} foi excluído com sucesso', 'success')
        return redirect(url_for('modelo'))
    flash(f'O modelo {modelo.name} não foi excluído', 'warning')
    return redirect(url_for('modelo'))

@app.route('/deletetema/<int:id>', methods=['GET','POST'])
def deletetema(id):
    tema = Tema.query.get_or_404(id)
    if request.method=='POST':
        db.session.delete(tema)
        db.session.commit()
        flash(f'O tema {tema.name} foi excluído com sucesso', 'success')
        return redirect(url_for('tema'))
    flash(f'O tema {tema.name} não foi excluído', 'warning')
    return redirect(url_for('tema'))

@app.route('/deleteproduto/<int:id>', methods=['GET','POST'])
def deleteproduto(id):
    produto = Addproduto.query.get_or_404(id)
    if request.method=='POST':
        if request.files.get('imagem_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_1))
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_2))
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_3))
             
            except Exception as e:
                print(f"Erro: {e}")   
            
        db.session.delete(produto)
        db.session.commit()
        flash(f'Produto {produto.nome} foi excluído com sucesso', 'success')  
        return redirect(url_for('admin'))
    flash(f'Produto {produto.nome} não foi excluído', 'success')    
    return redirect(url_for('admin'))



@app.route('/atualizartema/<int:id>', methods=['GET','POST'])
def atualizartema(id):
    if'email' not in session:
        flash(f'Favor efetuar o login', 'danger')
        return redirect(url_for('login'))
    atualizartema = Tema.query.get_or_404(id)
    tema = request.form.get('tema')
    if request.method=='POST':
        atualizartema.name = tema
        flash(f'O tema foi atualizado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('tema'))
    return render_template('/produtos/atualizarmodelo.html', title='Atualizar Temas', atualizartema=atualizartema)

@app.route('/atualizarproduto/<int:id>', methods=['GET','POST'])
def atualizarproduto(id):
    modelos = Modelo.query.all()
    temas = Tema.query.all()
    produto = Addproduto.query.get_or_404(id)
    modelo = request.form.get('modelo')
    tema = request.form.get('tema')
    form = Addprodutos(request.form)
    if request.method== "POST":
        produto.nome = form.nome.data
        produto.preco = form.preco.data
        produto.desconto = form.desconto.data
        produto.estoque = form.estoque.data
        produto.cor = form.cor.data
        produto.descricao = form.descricao.data
        produto.modelo_id = modelo
        produto.tema_id = tema

        if request.files.get('imagem_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_1))
                produto.imagem_1 = photos.save(request.files.get('imagem_1'),name=secrets.token_hex(10)+".")
            except:
                produto.imagem_1 = photos.save(request.files.get('imagem_1'),name=secrets.token_hex(10)+".")

        if request.files.get('imagem_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_2))
                produto.imagem_2 = photos.save(request.files.get('imagem_2'),name=secrets.token_hex(10)+".")
            except:
                produto.imagem_2 = photos.save(request.files.get('imagem_2'),name=secrets.token_hex(10)+".")

        if request.files.get('imagem_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/imagens/" + produto.imagem_3))
                produto.imagem_3 = photos.save(request.files.get('imagem_3'),name=secrets.token_hex(10)+".")
            except:
                produto.imagem_3 = photos.save(request.files.get('imagem_3'),name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'O produto foi atualizado com sucesso', 'success')
        return redirect('/admin')

    form.nome.data = produto.nome
    form.preco.data = produto.preco
    form.desconto.data = produto.desconto
    form.estoque.data = produto.estoque
    form.cor.data = produto.cor
    form.descricao.data = produto.descricao
   
    

    return render_template('/produtos/atualizarproduto.html', title='Atualizar Produtos', form=form, modelos=modelos, temas=temas, produto=produto, modelo=modelo, tema=tema)

#PAGINAS DE ACESSIBILIDADE

@app.route('/index1')
def home1():
    pagina = request.args.get('pagina',1, type=int)
    produtos = Addproduto.query.filter(Addproduto.estoque >0).order_by(Addproduto.id.desc()).paginate(page=pagina,per_page=4)    
    return render_template('produtos/index1.html', title='Pedcaneca - Canecas Personalizadas', produtos=produtos, modelos=modelos(), temas=temas())

@app.route('/search1', methods=['GET','POST'])
def search1():
    if request.method =='POST':
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        produtos = Addproduto.query.filter(Addproduto.nome.like(search)).all()
        return render_template('pesquisar1.html', produtos=produtos, modelos=modelos(), temas=temas())
    else:
        return redirect('/index1')
    
@app.route('/modelo1/<int:id>')
def get_modelo1(id):
    pagina = request.args.get('pagina',1, type=int)
    get_modelo1 = Modelo.query.filter_by(id=id).first_or_404()
    modelo = Addproduto.query.filter_by(modelo=get_modelo1).paginate(page=pagina,per_page=4)
    return render_template('produtos/index1.html', title='Pedcaneca - Canecas Personalizadas', modelo=modelo, modelos=modelos(), temas=temas(), get_modelo1=get_modelo1)

@app.route('/temas1/<int:id>')
def get_tema1(id):
    pagina = request.args.get('pagina',1, type=int)
    get_tema1 = Tema.query.filter_by(id=id).first_or_404()
    get_tema_prod = Addproduto.query.filter_by(tema=get_tema1).paginate(page=pagina,per_page=4)
    return render_template('produtos/index1.html', title='Pedcaneca - Canecas Personalizadas', get_tema_prod=get_tema_prod, temas=temas(), modelos=modelos(), get_tema1=get_tema1)

@app.route('/produto1/<int:id>')
def pagina_unica1(id):
    produto = Addproduto.query.get_or_404(id)
    return render_template('produtos/pagina_unica1.html', title='Pedcaneca - Canecas Personalizadas', produto=produto, modelos=modelos(), temas=temas())

