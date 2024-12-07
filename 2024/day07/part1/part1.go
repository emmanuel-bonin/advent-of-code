package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

func readFile() []string {
	const Filename = "../input.txt"

	file, err := os.Open(Filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	reader := bufio.NewReader(file)
	var lines []string
	for {
		line, _, err := reader.ReadLine()
		if err != nil {
			if err == io.EOF {
				break
			}
			panic(err)
		}
		lines = append(lines, string(line))
	}
	return lines
}

func generateOperations(nums []int, index int, currentResult int, results *[]int) {
	if index == len(nums) {
		*results = append(*results, currentResult)
		return
	}

	operators := []string{"+", "*"}
	for _, op := range operators {
		if op == "+" {
			newExpr := currentResult + nums[index]
			generateOperations(nums, index+1, newExpr, results)
		} else {
			newExpr := currentResult * nums[index]
			generateOperations(nums, index+1, newExpr, results)
		}
	}
}

func isValid(testVal int, operands []int) bool {
	var operations []int
	generateOperations(operands, 1, operands[0], &operations)
	for _, val := range operations {
		if val == testVal {
			return true
		}
	}
	return false
}

func main() {
	lines := readFile()
	result := 0
	for _, line := range lines {
		arr := strings.Split(line, ":")
		testVal, err := strconv.Atoi(arr[0])
		if err != nil {
			fmt.Printf("Error converting string %s to int\n", arr[0])
		}
		arr2 := strings.Split(arr[1], " ")

		var operands []int
		for _, val := range arr2 {
			if val != "" {
				val, err := strconv.Atoi(val)
				if err != nil {
					fmt.Printf("Error converting string %s to int\n", val)
				}
				operands = append(operands, val)
			}
		}
		if isValid(testVal, operands) {
			result += testVal
		}
	}
	fmt.Println(result)
}
