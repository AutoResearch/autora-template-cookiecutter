from autora.experimentalist.pooler.example_pooler import example_pool

# Note: We encourage you to adjust this test and write more functionality tests for your pooler.

def test_identity():
    sample = example_pool(2.0)
    assert sample == 2.0
