module.exports={
    404: function *(){
    	data = {title:"404 page not found"}
        yield this.render('err/404',data)
    },
    doContact: function *(){
        this.body={success: true}
    }
}