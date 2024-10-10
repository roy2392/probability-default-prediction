package main

import "fmt"

func main() {
	var accountBalance float64 = 1000

	fmt.Println("welcome to the bank")
	fmt.Println("How can I help you?")
	fmt.Println("1. check balance")
	fmt.Println("2. deposit")
	fmt.Println("3. withdraw")
	fmt.Println("4. exit")

	var choice int
	fmt.Scan(&choice)

	//wantsCheckBalance := choice == 1

	if choice == 1 {
		fmt.Println("Your balance is: ", accountBalance)
	}

	fmt.Println("You have selected: ", choice)
}
