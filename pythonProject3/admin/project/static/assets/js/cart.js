new Vue ({
    el: "#add",
    delimiters: ["[%","%]"],
    data:{



    },
    methods:{

        cart(id){

        token = document.querySelector("meta[name=csrf_token]").getAttribute("content")
        console.log(token)
        axios.post('mycart',{id:id},{
            headers:{
                "X-CSRFToken":token
            }
        }).then((r)=>{})



        },


        wish(id){

        tokenn = document.querySelector("meta[name=csrf_token]").getAttribute("content")
        console.log(tokenn)
        axios.post('wish',{id:id},{
            headers:{
                "X-CSRFToken":tokenn
            }
        }).then((r)=>{})



        }


    },
    created(){



    },
})