function clearClick()
{
    e = document.getElementById("listgroup");
    e.innerHTML = "";
};

// 等待html文档加载完后执行
$(document).ready(
    // 匿名函数，自动执行
    function()
    {
        $("#about-btn").click(
            function(event)
            {
                alert('use jquery');
            }
        );
    },

    // 鼠标悬浮在元素上面触发
    // hover接受两个函数
    $('p').hover(
        function()
        {
            $(this).css('color', 'red');
        },
        function()
        {
            $(this).css('color', 'blue');
        }
    ),

    // 添加类
    $('#button-about').addClass('btn btn-primary'),
    
    $('#button-about').click(
        function(event)
        {
            msgstr = $('#msg').html();
            msgstr = msgstr + '-append str';
            $('#msg').html(msgstr);
        }
    ),

    // 弹出大图
    $("#user_pic").click(
        function()
        {
            //$(this).imgbox();
            $(this).imgbox(
                {
                    'zoomOpacity'        : True,
                    'alignment'        : 'center',
                }
            );
        }
    ),

    // 弹出大图
    $("#index_picture").click(
        function()
        {
            //$(this).imgbox();
            $(this).imgbox(
                {
                    'zoomOpacity'        : True,
                    'alignment'        : 'center',
                }
            );
        }
    ),

    // 弹出大图
    $('.innerimg').click(
        function(e)
        {
            alert('hellp')
            var img = '<img src="' + $('.thumb').attr("src") + '" />';
            alert(img);
            $('.bigerimg').html($(img).animate({height: '30%', width: '30%'}, 500));
        }
    ),
);