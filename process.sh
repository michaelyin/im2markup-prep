#!/bin/bash

echo 'start processing inkml files now'
python -m unittest net.wyun.tests.prep.test_batch.TestBatch.test_all
cd data
tar czf batch.tar.gz ./batch