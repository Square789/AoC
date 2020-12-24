#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>

#define CUP_AMOUNT 1000000

// gcc -Wall -O3
// Runs for 3 hours on my machine lol
// I know I could represent the cups as nodes and then have them be
// a linked list by screwing with pointers but at this point I'm too stubborn
// to do it

uint32_t playfield[CUP_AMOUNT] = {9, 4, 2, 3, 8, 7, 6, 1, 5};
uint32_t picked_up[3];

size_t lin_search(uint32_t *arr, size_t arln, uint32_t value, int *success) {
	for (size_t i = 0; i < arln; i++) {
		if (arr[i] == value) {
			*success = 0;
			return i;
		}
	}
	*success = -1;
	return 0;
}

uint32_t mod_ca(int32_t a) {
	int32_t r = a % CUP_AMOUNT;
	return r < 0 ? r + CUP_AMOUNT : r;
}

int main() {
	// Assuming the max in the base field is 9 and there are 9 cups in the base field
	for (uint32_t idx = 9; idx < CUP_AMOUNT; idx++) {
		playfield[idx] = idx + 1;
	}
	int lssuc;
	uint64_t final_res;
	uint32_t max_cup, min_cup, cur_cup, dest_cup;
	size_t cur_cup_idx, dest_cup_idx, shift_ring_start, ringlength; 

	max_cup = CUP_AMOUNT;
	min_cup = 1;

	cur_cup_idx = 0;
	cur_cup = playfield[0];
	for (size_t _ = 0; _ < 10000000; _++) {
		for (size_t offset = 0; offset < 3; offset++) {
			picked_up[offset] = playfield[mod_ca(cur_cup_idx + 1 + offset)];
		}
		dest_cup = cur_cup;
		do {
			dest_cup -= 1;
			if (dest_cup < min_cup) {
				dest_cup = max_cup;
			}
			lin_search(picked_up, 3, dest_cup, &lssuc);
		} while (!lssuc);
		dest_cup_idx = lin_search(playfield, CUP_AMOUNT, dest_cup, &lssuc);
		if (lssuc < 0) { return 1; }
		shift_ring_start = mod_ca(cur_cup_idx + 4);
		ringlength = mod_ca(dest_cup_idx - shift_ring_start + 1);
		for (size_t offset = 0; offset < ringlength; offset++) {
			playfield[mod_ca(shift_ring_start + offset - 3)] = playfield[mod_ca(shift_ring_start + offset)];
		}
		dest_cup_idx = mod_ca(dest_cup_idx - 3);
		for (size_t offset = 0; offset < 3; offset++) {
			playfield[mod_ca(dest_cup_idx + 1 + offset)] = picked_up[offset];
		}
		cur_cup_idx = mod_ca(cur_cup_idx + 1);
		cur_cup = playfield[cur_cup_idx];
		if ((_ & 0xFFF) == 0xFFF) printf(".");
	}

	cur_cup_idx = lin_search(playfield, CUP_AMOUNT, 1, &lssuc);
	printf("\n%u, %u", playfield[mod_ca(cur_cup_idx + 1)], playfield[mod_ca(cur_cup_idx + 2)]);
	final_res = (uint64_t)playfield[mod_ca(cur_cup_idx + 1)] * (uint64_t)playfield[mod_ca(cur_cup_idx + 2)];
	printf("\n%I64u\n", final_res);

	return 0;
}