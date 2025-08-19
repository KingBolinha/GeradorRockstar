import { MailSlurp } from 'mailslurp-client';
import * as cheerio from 'cheerio';
import keypress from 'keypress';
import chalk from 'chalk';
import { exec } from 'child_process';
import clipboardy from 'clipboardy';
import figlet from 'figlet';

// Função para exibir o título estilizado
function printTitle() {
    console.clear();
    figlet.text('Wolf Rockstar', {
        font: 'Standard',
        horizontalLayout: 'default',
        verticalLayout: 'default',
        width: 80,
        whitespaceBreak: true,
    }, (err, data) => {
        if (err) {
            console.error('Erro ao gerar texto estilizado:', err);
            return;
        }
        console.log(chalk.green(data));
        console.log(chalk.bold.redBright('Version: 2.2'));
        console.log(chalk.bold.magenta('Created by PEITANOVE® & KINGBOLINHA'));
    });
}

// Configurações do MailSlurp
const apiKey = 'a5371c5f41ccaab0cd1cb1e3928b29a4395bb0cfc3f4823bb0ed14a1f2ae932e'
const mailslurp = new MailSlurp({ apiKey, timeout: 120000 });

let currentInboxId = null;
let currentEmailAddress = null;
let rockstarCodeSent = {};

// Copiar texto para clipboard
async function copyToClipboard(content) {
    try {
        clipboardy.writeSync(content);
        console.log(chalk.green(`Conteúdo copiado para a área de transferência: ${content}`));
    } catch (error) {
        console.error(chalk.red('Erro ao copiar conteúdo para a área de transferência:'), error);
    }
}

// Testa conexão com API MailSlurp
async function testConnection() {
    try {
        await mailslurp.getInboxes();
        console.log(chalk.green('Conexão com API bem-sucedida.'));
    } catch (error) {
        console.error(chalk.red('Falha ao conectar com API:'), error);
        process.exit(1);
    }
}

// Cria inbox simples (grátis) com email aleatório
async function createInbox() {
    try {
        const inbox = await mailslurp.createInbox();
        currentInboxId = inbox.id;
        currentEmailAddress = inbox.emailAddress;
        printTitle();
        console.log(chalk.blue(`Novo e-mail gerado: ${currentEmailAddress}`));
        await copyToClipboard(currentEmailAddress);
    } catch (error) {
        console.error(chalk.red('Erro ao criar caixa de entrada:'), error);
    }
}

// Busca e-mails da inbox atual
async function getEmails(inboxId) {
    try {
        const emails = await mailslurp.getEmails(inboxId, { limit: 10 });
        return emails;
    } catch (error) {
        console.error(chalk.red('Erro ao recuperar e-mails:'), error);
        return [];
    }
}

// Extrai código de 6 dígitos do corpo do email (ajuste regex se precisar)
function extractRockstarCode(emailBody) {
    const codeMatch = emailBody.match(/\b\d{6}\b/);
    return codeMatch ? codeMatch[0] : '';
}

// Verifica se tem email novo com código da Rockstar
async function checkForVerificationCode() {
    if (!currentInboxId) return;

    try {
        const emails = await getEmails(currentInboxId);
        if (!emails || emails.length === 0) return;

        for (const email of emails) {
            if (email.subject && email.subject.includes('Seu código de verificação da Rockstar Games')) {
                if (!rockstarCodeSent[email.id]) {
                    const emailDetails = await mailslurp.getEmail(email.id);
                    const code = extractRockstarCode(emailDetails.body);
                    if (code) {
                        rockstarCodeSent[email.id] = true;
                        printTitle();
                        console.log(chalk.green(`Código de verificação da Rockstar Games: ${code}`));
                        await copyToClipboard(code);
                    }
                }
            }
        }
    } catch (error) {
        console.error(chalk.red('Erro ao verificar e-mails:'), error);
    }
}

// Polling para verificar emails novos a cada 5 segundos
function startPolling() {
    setInterval(checkForVerificationCode, 5000);
}

// Controle de teclado
function promptUser() {
    keypress(process.stdin);

    process.stdin.on('keypress', async (ch, key) => {
        if (key) {
            switch (key.name) {
                case 'q':
                    printTitle();
                    console.log(chalk.cyan('Gerando um novo e-mail...'));
                    await createInbox();
                    break;
                case '2':
                    printTitle();
                    console.log(chalk.cyan('Verificando e-mails...'));
                    await checkForVerificationCode();
                    break;
                case 'c':
                    printTitle();
                    console.clear();
                    console.log(chalk.magenta('Saindo...'));
                    process.exit();
                    break;
                case 'r':
                    printTitle();
                    console.log(chalk.yellow('Executando outro script Python...'));
                    exec('py bypass3.py', handlePythonExecution);
                    break;
                default:
                    printTitle();
                    console.log(chalk.red('Tecla inválida. Tente novamente.'));
                    break;
            }
        }
    });

    process.stdin.setRawMode(true);
    process.stdin.resume();
}

function handlePythonExecution(error, stdout, stderr) {
    if (error) {
        console.error(chalk.red(`Erro ao executar o script Python: ${error.message}`));
        return;
    }
    if (stderr) {
        console.error(chalk.red(`stderr: ${stderr}`));
        return;
    }
    console.log(chalk.green(`stdout: ${stdout}`));
}

// Execução principal
(async () => {
    printTitle();
    await testConnection();
    await createInbox();
    startPolling();
    promptUser();
})();