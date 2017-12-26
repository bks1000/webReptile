//种子清洗
//种子文件结构：：http://blog.csdn.net/csupengu/article/details/8673666
//采用nodejs 的 parse-torrent模块
//模块安装:npm install parse-torrent
//程序运行：node washTorrent.js(当前目录下)
////安装模块：npm install iconv-lite(中文支持)[nodejs原生对utf8支持]

// 加载File System读写模块  
var fs = require('fs');
// 加载编码转换模块  
//var iconv = require('iconv-lite');
//加载种子解析模块
var parseTorrent = require('parse-torrent');

var info0 = parseTorrent(fs.readFileSync('F:/HW/OCU27Fz.torrent'));
//console.log(info.name);
//console.log(info.files);

//console.log(getType(info));

var file ="F:/HW/torrent.txt";
//writeFile(file,info.files[0].path);
//测试，查看输出
//var s = JSON.stringify(info);//把objec序列化
//writeFile(file,s);
//return;
var buf = parseTorrent.toTorrentFile({
    info: cleanInfo(info0)
});
//写入新的torrent
fs.writeFile("F:/HW/" + info0.name + ".torrent", buf);

//compareTorrent(info,buf);//输出差别


//清除不必要的种子文件中的文件信息[info :种子文件]
function cleanInfo(info){
    var files = info.files;
    var indexs=[];//记录要删除的种子内的文件索引
    for(var i=0;i<files.length;i++){
        var f = files[i];
        //测试，将全部内容输出到文本文件(windows平台)
        //writeFile(file,"path:"+f.path+"\r\n name:"+f.name+"\r\n length:"+f.length+"\r\n offset:"+f.offset);
        for(var key in f){
            if(key=="path"){
                var p = f.path;
                //console.log(p);
                //console.log(p.slice(-3));//获取扩展名
                var extend=p.slice(-3);
                if(extend=="url"||extend=="rar"||extend=="txt"||extend=="URL"||extend=="mht"||extend=="jpg"||extend=="gif"){
                    //标记删除
                    indexs.push(i);
                    //console.log(p);
                }
            }
        }
    }
    //不好删除某个索引对应的数组元素，所以，重新组织一个文件列表
    var newFiles = [];
    for(var i=0;i<files.length;i++){
        if(indexs.indexOf(i)==-1){
            console.log(files[i].path)
            //如果元素不存在标记删除的索引数组中，将其添加到新数组中
            newFiles.push(files[i]);
        }
    }
    info.files = newFiles;
    return info;
}

//检查变量类型
function getType(o) { 
    var _t; return ((_t = typeof(o)) == "object" ? o==null && "null" || Object.prototype.toString.call(o).slice(8,-1):_t).toLowerCase(); 
} 


//写文件
function writeFile(file,data){  
    // 测试用的中文  
    //var str = "\r\n我是一个人Hello myself!"; 
    // 把中文转换成字节数组  
    //var arr = iconv.encode(str, 'gbk');  
    //console.log(arr);  
    arr = data;
    // appendFile，如果文件不存在，会自动创建新文件  
    // 如果用writeFile，那么会删除旧文件，直接写新文件  
    fs.appendFile(file, arr, function(err){  
        if(err)  
            console.log("fail " + err);  
        else  
            console.log("写入文件ok");  
    });  
} 

//两个种子文件内容比对(测试修改前和修改后的差别)
function compareTorrent(info,info2){
    console.log("announce:");
    console.log(info.announce);
    console.log("announce2:");
    console.log(info2.announce);
} 

//未使用  
function readFile(file){  
    fs.readFile(file, function(err, data){  
        if(err)  
            console.log("读取文件fail " + err);  
        else{  
            // 读取成功时  
            // 输出字节数组  
            console.log(data);  
            // 把数组转换为gbk中文  
            //var str = iconv.decode(data, 'gbk');  
            console.log(data);  
        }  
    });  
}  