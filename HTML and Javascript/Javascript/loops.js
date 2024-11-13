for (let i = 0; i <= 20;i++) {
    console.log(i)
}

console.log();

for (let i = 3; i <= 29;i++) {
    if (i%2 == 1) {
        console.log(i)
    }
}

console.log();

for (let i = 12; i >= -14;i--) {
    if (i%2 == 0) {
        console.log(i)
    }
}

console.log();

for (let i = 50; i >= 20;i--) {
    if (i%3 == 0) {
        console.log(i)
    }
}

console.log();

let oddoreven_num = 3
if (oddoreven_num%2 == 0) {
    console.log(oddoreven_num,"is even")
} else {
    console.log(oddoreven_num,"is odd")
}

console.log();

let posorneg_num = -12
if (posorneg_num > 0) {
    console.log(posorneg_num,"is positive")
} else {
    console.log(posorneg_num,"is negative")
}

console.log();

let num_1 = 2
let num_2 = 7
if (num_1 > num_2) {
    console.log(num_1,"is larger than",num_2)
} else {
    console.log(num_2,"is larger than",num_1)
}

