const mineflayer = require('mineflayer');
const fs = require('fs');
const host = process.argv[2];
const port = parseInt(process.argv[3]);
const version = process.argv[4];
const username = process.argv[5];
const commandsFile = process.argv[6];
let commands = [];
if (commandsFile) {
    try {
        const data = fs.readFileSync(commandsFile, 'utf8');
        commands = data.split(/\r?\n/).filter(l => l.trim().length > 0);
    } catch(e) {}
}
const bot = mineflayer.createBot({ host, port, username, version });
bot.on('spawn', async () => {
    for (let cmd of commands) {
        bot.chat(cmd);
        await new Promise(resolve => setTimeout(resolve, 3500));
    }
});
bot.on('error', console.error);
bot.on('end', () => process.exit(0));