#target photoshop

// Função para ler dados de um arquivo CSV
function readCSV(filePath) {
    var file = new File(filePath);
    var data = [];

    if (file.open('r')) {
        while (!file.eof) {
            var line = file.readln();
            var columns = line.split(';');
            data.push({
                psd: columns[0],
                image: columns[1]
            });
        }
        file.close();
    } else {
        errorLog.push("Erro ao abrir o arquivo CSV: " + filePath);
    }

    return data;
}

// Função para salvar o log de erros em arquivo TXT
function salvarLogDeErros(caminhoLog, erros) {
    var file = new File(caminhoLog);
    if (file.open('w')) {
        for (var i = 0; i < erros.length; i++) {
            file.writeln(erros[i]);
        }
        file.close();
    } else {
        alert("Erro ao salvar o arquivo de log.");
    }
}

// Lista para armazenar os erros
var errorLog = [];

// Caminhos
var csvPath = "C:/Users/User/Desktop/robo unir fotos/planilha.csv";
var logPath = "C:/Users/User/Desktop/robo unir fotos/log_erros.txt";

// Ler os dados do CSV
var fileData = readCSV(csvPath);

// Processar cada linha da planilha
for (var i = 0; i < fileData.length; i++) {
    try {
        var psdFilePath = new File("C:/Users/User/Desktop/robo unir fotos/produtos/" + fileData[i].psd);
        var imageFilePath = new File("C:/Users/User/Desktop/robo unir fotos/carros pronto/" + fileData[i].image);

        if (!psdFilePath.exists) {
            errorLog.push("Erro: O arquivo PSD não foi encontrado: " + psdFilePath.fsName);
            continue;
        }

        if (!imageFilePath.exists) {
            errorLog.push("Erro: A imagem não foi encontrada: " + imageFilePath.fsName);
            continue;
        }

        var doc = app.open(psdFilePath);
        var imageFile = app.open(imageFilePath);

        imageFile.selection.selectAll();
        imageFile.selection.copy();
        imageFile.close(SaveOptions.DONOTSAVECHANGES);

        var newLayer = doc.artLayers.add();
        newLayer.name = "Nova Camada";

        doc.paste();
        doc.save();
        doc.close(SaveOptions.SAVECHANGES);
        
    } catch (e) {
        errorLog.push("Erro inesperado ao processar linha " + (i+1) + ": " + e.message);
    }
}

// Salvar os erros após terminar
if (errorLog.length > 0) {
    salvarLogDeErros(logPath, errorLog);
}
