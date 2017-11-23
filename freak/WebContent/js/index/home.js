function bigImg1(x)
{
	x.innerHTML = "用户&nbsp;&nbsp;&nbsp;<i class=\"icon-user\"></i>";
}

function normalImg1(x)
{
	x.innerHTML = "<i class=\"icon-user\"></i>";
}

function bigImg2(x)
{
	x.innerHTML = "列表&nbsp;&nbsp;&nbsp;<i class=\"icon-list icon-white\"></i>";
}

function normalImg2(x)
{
	x.innerHTML = "<i class=\"icon-list icon-white\"></i>";
}

function bigImg3(x)
{
	x.innerHTML = "聊天&nbsp;&nbsp;&nbsp;<i class=\"icon-comment icon-white\"></i>";
}

function normalImg3(x)
{
	x.innerHTML = "<i class=\"icon-comment icon-white\"></i>";
}

function bigImg4(x)
{
	x.innerHTML = "编辑&nbsp;&nbsp;&nbsp;<i class=\"icon-edit icon-white\"></i>";
}

function normalImg4(x)
{
	x.innerHTML = "<i class=\"icon-edit icon-white\"></i>";
}

function bigImg5(x)
{
	x.innerHTML = "回收站&nbsp;&nbsp;&nbsp;<i class=\"icon-trash icon-white\"></i>";
}

function normalImg5(x)
{
	x.innerHTML = "<i class=\"icon-trash icon-white\"></i>";
}

function bigImg6(x)
{
	x.innerHTML = "退出&nbsp;&nbsp;&nbsp;<i class=\"icon-off icon-white\"></i>";
}

function normalImg6(x)
{
	x.innerHTML = "<i class=\"icon-off icon-white\"></i>";
}

function bigImg7(x)
{
	x.innerHTML = "神秘的传送门&nbsp;&nbsp;&nbsp;<i class=\"icon-gift icon-white\"></i>";
}

function normalImg7(x)
{
	x.innerHTML = "<i class=\"icon-gift icon-white\"></i>";
}

function send() 
{
	$.post("connect.do", 
		{
			
		},
	    function(result) {
			alert("success");
	    });
}
