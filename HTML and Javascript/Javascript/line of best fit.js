let coords = [[8,3],[2,10],[11,3],[6,6],[5,8],[4,12],[12,1],[9,4],[6,9],[1,14]];
let x_ = 0;
let y_ = 0;
for (i=0;i<coords.length;i++){
    x_ += coords[i][0]
    y_ += coords[i][1]
};
x_ = x_/coords.length;
y_ = y_/coords.length;
let numerator = 0;
let denominator = 0;
for (i=0;i<coords.length;i++){
    numerator += (coords[i][0]-x_)*(coords[i][1]-y_)
    denominator += (coords[i][0]-x_)**2
};
let slope = numerator/denominator;
let y_int = y_ - (slope*x_);
console.log(`Line of best fit: y = ${Math.round(slope*10)/10}x + ${Math.round(y_int*10)/10}`);


