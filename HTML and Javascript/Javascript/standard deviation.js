let sets = [[20,21,19,22,21,20,19,20,21,20],[303,299,306,298,304,307,299,302,305,299,300],[15.3,14.9,15.1,15.2,14.8,14.7,15.1,14.8,15.0,15.0],[87,89,84,88,89,87,86,87,86,87]]
for (n = 0; n < sets.length; n++){
    StandardDeviationCalculation(sets[n])
}
function StandardDeviationCalculation(set){
let total = 0
for (let i = 0; i < set.length; i++){
    total += set[i]
}
let mean = total/set.length
let squaresum = 0
for (let i=0; i < set.length; i++){
    squaresum += (set[i] - mean)**2
}
let standard_deviation = Math.sqrt(squaresum/(set.length-1))
console.log("The standard deviation of the set",set,"is",standard_deviation,"with a mean of",mean)}