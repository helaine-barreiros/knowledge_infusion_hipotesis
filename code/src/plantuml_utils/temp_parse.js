
        const { parse } = require('plantuml-parser');
        
        const data = process.argv[2];
        const result = parse(data);
        console.log(JSON.stringify(result));
        