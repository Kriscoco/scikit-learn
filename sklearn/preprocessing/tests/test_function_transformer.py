from nose.tools import assert_equal
import numpy as np

from sklearn.preprocessing import FunctionTransformer


def _make_func(args_store, kwargs_store, func=lambda X, *a, **k: X):
    def _func(X, *args, **kwargs):
        args_store.append(X)
        args_store.extend(args)
        kwargs_store.update(kwargs)
        return func(X)

    return _func


def test_delegate_to_func():
    # (args|kwargs)_store will hold the positional and keyword arguments
    # passed to the function inside the FunctionTransformer.
    args_store = []
    kwargs_store = {}
    X = np.arange(10).reshape((5, 2))
    np.testing.assert_array_equal(
        FunctionTransformer(_make_func(args_store, kwargs_store)).transform(X),
        X,
        'transform should have returned X unchanged',
    )

    # The function should only have recieved X.
    assert_equal(
        args_store,
        [X],
        'Incorrect positional arguments passed to func: {args}'.format(
            args=args_store,
        ),
    )
    assert_equal(
        kwargs_store,
        {},
        'Unexpected keyword arguments passed to func: {args}'.format(
            args=kwargs_store,
        ),
    )

    # reset the argument stores.
    args_store[:] = []  # python2 compatible inplace list clear.
    kwargs_store.clear()
    y = object()

    np.testing.assert_array_equal(
        FunctionTransformer(
            _make_func(args_store, kwargs_store),
            pass_y=True,
        ).transform(X, y),
        X,
        'transform should have returned X unchanged',
    )

    # The function should have recieved X and y.
    assert_equal(
        args_store,
        [X, y],
        'Incorrect positional arguments passed to func: {args}'.format(
            args=args_store,
        ),
    )
    assert_equal(
        kwargs_store,
        {},
        'Unexpected keyword arguments passed to func: {args}'.format(
            args=kwargs_store,
        ),
    )


def test_np_log():
    X = np.arange(10).reshape((5, 2))

    # Test that the numpy.log example still works.
    np.testing.assert_array_equal(
        FunctionTransformer(np.log1p).transform(X),
        np.log1p(X),
    )
