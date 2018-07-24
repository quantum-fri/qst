import numpy as np
import sys

file_list = ['d','a', 'r', 'l', 'h','v']

# dark counts from lights off laser off
dark_mean = 6.236
dark_std = 2.714
dark_num = 1008

def get_mean_num_var(file_base, path):
    temp = []
    print(file_base, end=' ')
    for i in range(1,3):
        filename = path + '/' + file_base + str(i) + '.txt'
        try:
            lines = [line.rstrip('\n') for line in open(filename)]
        except FileNotFoundError:
            print('file %s not found!' % filename)
            sys.exit()
        lines = lines[23:]
        num_data = len(lines)
        total = 0
        for line in lines:
            total += int(line.split()[1])
        mean = total/num_data
        var_sum = 0
        for line in lines:
            var_sum += (mean - int(line.split()[1]))**2
        var = var_sum/(num_data - 1)
        temp.append([mean, num_data, var])
    new_avg = (temp[0][0] + temp[1][0])/2
    new_std = (temp[0][1] + temp[1][1])/2
    new_count = temp[0][2] + temp[1][2]
    return [new_avg, new_std, new_count]

def fidelity(stokes_params, expected):
    expected = np.array(expected)
    pMatrix = np.array(densityMatrix(stokes_params))
    fid = np.dot(expected.conj(), np.dot(pMatrix, expected))
    return np.real(fid)

def error_prop(parameters, function, errors):
    def error_prop_recurse(params, f, etas):
        if len(params) == 0: return [f([])]
        
        out = []
        for x in [params[0] + etas[0], params[0] - etas[0]]:
            fnew = lambda inParams: f([x]+inParams)
            out += error_prop_recurse(params[1:], fnew, etas[1:])
        return out

    ZH = function(*parameters)
    errorMax = 0

    fnew = lambda inParams: function(*inParams)
    deviations = error_prop_recurse(parameters, fnew, errors)
    for deviation in deviations:
        if np.real(abs(deviation - ZH)) > np.real(errorMax): errorMax = abs(deviation - ZH)
    return ZH, errorMax

def densityMatrix(params): 
    rho = np.eye(2).astype(complex)/2
    rho += np.array([[0,1],[1,0]])*params[0]/2
    rho += np.array([[0,-1j],[1j,0]])*params[1]/2
    rho += np.array([[1,0],[0,-1]])*params[2]/2
    return rho

def standard_error(variance, sample_size):
    return 1.96*(variance/sample_size)**(0.5)

def get_estimator(basis_1, basis_2, dark):
    return (basis_1 - dark)/(basis_1 + basis_2 - 2*dark)

def pedantic_error(result_list):
    se_dark = standard_error(dark_std**2, dark_num)
    stokes_params = []
    stokes_errors = []
    for i in range(0, len(result_list), 2):
        se_basis_1 = standard_error(result_list[i][2], result_list[i][1])
        se_basis_2 = standard_error(result_list[i+1][2], result_list[i+1][1])
        error = error_prop([result_list[i][0], result_list[i+1][0], dark_mean], get_estimator, [se_basis_1, se_basis_2, se_dark])[1]
        stokes_errors.append(error)
        expected = 2 * get_estimator(result_list[i][0], result_list[i+1][0], dark_mean) - 1
        stokes_params.append(expected)
    return stokes_params, stokes_errors

def normalize(params, errs):
    length = (params[0]**2 + params[1]**2 + params[2]**2)**(0.5)
    if (length > 1): 
        diff = abs(1 - length)
        normalized = [x/length for x in params]
        errors = []
        for err in errs:
            errors.append(abs(diff + err))
        return normalized, errors
    else: 
        return params, errs

if __name__ == '__main__': 
    if len(sys.argv) < 2: 
        print('missing folder argument')
        sys.exit()
    expected = [1/(2**0.5),complex(0,1/(2**0.5))]
    result_list = []
    for basis in file_list:
        results = get_mean_num_var(basis, sys.argv[1])
        print('counts/bin: %.2f' % results[0])
        result_list.append(results)

    stokes_params, stokes_errors = pedantic_error(result_list)
    f = lambda x,y,z: fidelity([x,y,z], expected)
    stokes_params, stokes_errors = normalize(stokes_params, stokes_errors)
    fid, err = error_prop(stokes_params, f, stokes_errors)
    
    print('')
    for i in range(0,3):
        print('S%d: %.4f ± %.4f' % (i+1, stokes_params[i], stokes_errors[i]))
    print('fidelity: ', fid, '+-', err)
    length = (stokes_params[0]**2 + stokes_params[1]**2 + stokes_params[2]**2)**(0.5)
    print('length: %.4f' % length)

    expected = np.array(expected)
    print('\ninput pure state: ' + str(expected))
    print('expected X:', np.dot(expected.conj(), np.dot(np.array([[0,1],[1,0]]), expected)))
    print('expected Y:', np.dot(expected.conj(), np.dot(np.array([[0,-1j],[1j,0]]), expected)))
    print('expected Z:', np.dot(expected.conj(), np.dot(np.array([[1,0],[0,-1]]), expected)))
