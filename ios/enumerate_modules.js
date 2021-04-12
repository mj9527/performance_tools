var modules = Process.enumerateModules();
for(var i = 0; i < modules.length; i++ ) {
    console.log(JSON.stringify(modules[i]));
}