/* log1p 10-601A 
/* Author: Jerry Bai
 */
#include <stdio.h>    
#include <math.h>

double log_sum(double left, double right)
{
	if (right < left) {
		return left + log1p(exp(right - left));
	} else if (left < right) {
		return right + log1p(exp(left - right));
	}
	return left + log1p(1.0);
}