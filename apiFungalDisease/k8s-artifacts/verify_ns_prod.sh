#!/bin/bash

if kubectl get ns -o custom-columns=:metadata.name | grep -q 'NAMESPACE'; then
	echo "NAMESPACE namespace already exists"
else
    kubectl create ns NAMESPACE
fi
