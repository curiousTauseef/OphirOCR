
function color(img) {
    var data=img.data;
    function isBlack(x,y){
        x = (x+img.width)%img.width;
        y = (y+img.height)%img.height;
        return data[4*(y*img.width+x)+3]>200;
    }
    function setRed(x,y) {
        x = (x+img.width)%img.width;
        y = (y+img.height)%img.height;
        data[4*(y*img.width+x)]=255;
        data[4*(y*img.width+x)+3]=255;
    }
    var x=0, y=0, chemin=[],maxi=0;
    while (true) {
            x = (x+img.width)%img.width;
        y = (y+img.height)%img.height;
        chemin.push([x,y]);
        setRed(x,y);
        if (!isBlack(x+1,y)) x++;
        else if (!isBlack(x,y+1)) y++;
        else if (!isBlack(x-1,y)) x--;
        else if (!isBlack(x,y-1)) y--;
        else {
            chemin.pop();
            if (chemin.length==0)break;
            var xy = chemin.pop();
            x = xy[0]; y = xy[1];
        }
        maxi++;
        if (maxi > 2*(img.width*img.height)){
            console.log("Taking too long...")
            break;
            
        }
    }
    console.log("pixels visités/nbre pixels",maxi/(img.width*img.height));
    return img;
}
