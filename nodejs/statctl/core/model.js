module.exports = function(app,fs,root){
		md = {};

    fs.readdirSync(C.model).forEach(function (name) {
        var modelExt = '.js'
        if(name.indexOf(modelExt)>-1) {
            var model = require(C.model + name)
            name = name.replace(modelExt, '').toLowerCase()

            //mongoose
            
            md[name] = model;

        }

    })
    md.base = require('./function/init')(root)

		return md
}