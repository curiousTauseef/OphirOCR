function AlphaLevelArea (imageData, x0,y0,width,height, convertToGreyScale) {
    //Provides easy access to the alpha (opacity) components of an area of an ImageData
    //If convertToGreyScale is set to true, imageData will be converted to have its
    //alpha components matching it's grey level
    var data = imageData.data,
        maxWidth = imageData.width,
        xmin = x0 || 0,
        ymin = y0 || 0;
        
    this.width = width || imageData.width;
    this.height = height || imageData.height;

    if (convertToGreyScale) {
        for(var i=3;i<data.length;i+=4){
            data[i] *= 1-(data[i-1]+data[i-2]+data[i-3])/765; //3*255=765
        }
    }

    this.getPixel = function (x,y) {
        if (y>=height||x>=width) throw "Coordonnées invaldes";
        return data[4*((y+ymin)*maxWidth+x+xmin)+3];
    };
    this.crop = function (x,y,w,h) {
        this.width = w; this.height = h; xmin += x; ymin += y;
    };
    this.surround = function(ctx) {
        ctx.strokeRect(xmin,ymin,this.width,this.height);
    }
    this.subArea = function (x,y,w,h) {
        return new AlphaLevelArea(imageData,xmin+x,ymin+y,w,h);
    }
}


AlphaLevelArea.prototype.auto_crop = function () {
//Finds the borders of the image content
    var bounds = {x:0,y:0,width:0,height:0},
        x,y;
    //    X axis
    for(x=0; x<this.width; x++){
        for(y=0;y<this.height;y ++) {
            if (this.getPixel(x,y) !== 0) {bounds.x = x; break}
        }
        if(bounds.x) break;
    }
    if(!bounds.x) {this.crop(0,0,0,0); return bounds} //The area contains nothing
    for(var x=this.width-1; x>=0; x--) {
        for(var y=0;y<this.height;y ++) {
            if (this.getPixel(x,y) !== 0) {bounds.width = x-bounds.x+1; break }
        }
        if(bounds.width) break;
    }

    //    Y axis
    for(var y=0;y<this.height; y++){
        for(var x=bounds.x; x<bounds.x+bounds.width;x ++) {
            if (this.getPixel(x,y) !== 0) {bounds.y = y; break}
        }
        if(bounds.y) break;
    }
    for(var y=this.height-1;y>=0; y--){
        for(var x=bounds.x; x<bounds.x+bounds.width;x ++) {
            if (this.getPixel(x,y) !== 0) {bounds.height = y-bounds.y+1; break;}
        }
        if(bounds.height) break;
    }
    this.crop(bounds.x,bounds.y,bounds.width,bounds.height);
    return bounds;
}
