"""You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1:
Input: n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps

Example 2:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step"""

def climbStairs(total_steps):
    if total_steps == 1:
        return 1

    one_step_before = 2   
    two_steps_before = 1  

    for current_step in range(3, total_steps + 1):
        current_ways = one_step_before + two_steps_before
        two_steps_before = one_step_before
        one_step_before = current_ways

    return one_step_before

print(climbStairs(5))