// src/cpp/fast_ops.cpp
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

double fast_sum(py::array_t<double> input)
{
    auto buf = input.request();
    double *ptr = static_cast<double *>(buf.ptr);
    double sum = 0;

    for (size_t i = 0; i < buf.size; i++)
    {
        sum += ptr[i];
    }

    return sum;
}

PYBIND11_MODULE(libnm_c, m)
{
    m.doc() = "Fast operations using C++";
    m.def("fast_sum", &fast_sum, "Quickly sum an array of doubles");
}