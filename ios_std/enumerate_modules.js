const modules = Process.enumerateModules();
for(let i = 0; i < modules.length; i++) {
    console.log(JSON.stringify(modules[i]));
}
