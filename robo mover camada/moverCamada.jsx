

#target photoshop

// Pasta com os arquivos PSD
var pasta = Folder.selectDialog("Selecione a pasta com os arquivos PSD");

if (pasta != null) {
    var arquivos = pasta.getFiles("*.psd");

    for (var i = 0; i < arquivos.length; i++) {
        var doc = open(arquivos[i]);

        try {
            var camadasAlvo = [];

            // Coleta todas as camadas com o nome "Nova Camada"
            for (var j = 0; j < doc.artLayers.length; j++) {
                if (doc.artLayers[j].name == "Nova Camada") {
                    camadasAlvo.push(doc.artLayers[j]);
                }
            }

            // Define as posições com base na quantidade de camadas
            var posicoes = [];

            switch (camadasAlvo.length) {
                case 1:
                    posicoes = [[500, 1000]];
                    break;
                case 2:
                    posicoes = [[800, 1000], [5, 1000]];
                    break;
                case 3:
                    posicoes = [[800, 1000], [500, 1000], [5, 1000]];
                    break;
                case 4:
                    posicoes = [[900, 1000], [600, 1000], [200, 1000], [5, 1000]];
                    break;
                case 5:
                    posicoes = [[1100, 1000], [800, 1000], [540, 1000], [240, 1000], [5, 1000]];
                    break;
                // Adicione mais conforme necessidade
                default:
                    alert("Arquivo " + doc.name + " tem " + camadasAlvo.length + " camadas 'Nova Camada', mas nenhuma posição foi definida.");
                    break;
            }

            for (var k = 0; k < camadasAlvo.length && k < posicoes.length; k++) {
                var camada = camadasAlvo[k];
                var alvoX = posicoes[k][0];
                var alvoY = posicoes[k][1];

                var deslocX = alvoX - camada.bounds[0].as("px");
                var deslocY = alvoY - camada.bounds[1].as("px");

                camada.translate(deslocX, deslocY);
            }

            doc.save();
        } catch (e) {
            alert("Erro ao processar: " + doc.name + "\n" + e.message);
        }

        doc.close(SaveOptions.SAVECHANGES);
    }

    alert("Processamento concluído!");
}