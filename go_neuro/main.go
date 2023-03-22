package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"math/rand"
	"os"

	"github.com/goml/gobrain"
)

type User struct {
	Need     float64
	Previous float64
	Value    float64
}

func main() {

	filename, err := os.Open("result.json")
	if err != nil {
		log.Fatal(err)
	}

	defer filename.Close()

	data, err := ioutil.ReadAll(filename)

	if err != nil {
		log.Fatal(err)
	}

	var json_result []User

	jsonErr := json.Unmarshal(data, &json_result)

	if jsonErr != nil {
		log.Fatal(jsonErr)
	}
	// set the random seed to 0
	rand.Seed(0)

	// create the XOR representation patter to train the network
	patterns := [][][]float64{}
	for i := 0; i < len(json_result); i++ {
		temp := [][]float64{
			{
				json_result[i].Previous,
				json_result[i].Value,
			},
			{
				json_result[i].Need,
			},
		}
		patterns = append(patterns, temp)
	}
	//fmt.Println(patterns)
	// instantiate the Feed Forward
	ff := &gobrain.FeedForward{}

	// initialize the Neural Network;
	// the networks structure will contain:
	// 2 inputs, 2 hidden nodes and 1 output.
	ff.Init(2, 10, 1)

	// train the network using the XOR patterns
	// the training will run for 1000 epochs
	// the learning rate is set to 0.6 and the momentum factor to 0.4
	// use true in the last parameter to receive reports about the learning error
	ff.Train(patterns, 500000, 0.6, 0.4, true)
	ff.Test(patterns)

	// inputs to send to the neural network
	inputs := [][]float64{
		{80.8266, 80.7426}, // 0
		{13.3235, 13.2788}, // 0
		{15.2983, 15.3808}, // 1
		{15.3808, 15.4673}, // 1
	}
	answ := []float64{
		0, 0, 1, 1,
	}

	var result []float64
	for i := 0; i < len(inputs); i++ {
		// saves the result
		result = ff.Update(inputs[i])

		// prints the result
		fmt.Println(result[0], math.Round(result[0]) == answ[i])
	}
}

/*
5000:

0.5647454764641688 -
0.6854666187690484 -
0.6822866686161985 +
0.6822349694668296 +


50000:

0.7707474222448885 -
0.7707474226149744 -
0.7707474223229693 +
0.7707474223220222 +

100000:
0.7707474224639816
0.7707474220561369
0.7707474224459417
0.7707474224480876
*/
