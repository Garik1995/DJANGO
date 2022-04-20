new Vue ({
    el: "#app",
    delimiters: ["[%","%]"],
    data:{



    },
    methods:{

    function send(id){
        let feedback = document.getElementById(feedback).value
//        console.log(feedback)
//        console.log(id)
        token = document.querySelector("meta[name=csrf_token]").getAttribute('countent')
        axios.post('/feedback',{feedback:feedback,id:id},{
            headers:{
                "X-CSRFToken":token
            }
        }).then((r)=>{})
//        console.log(r)
        })

    }


        },

    created(){



    },
})