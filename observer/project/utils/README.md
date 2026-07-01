# 

## ObserverRunner is the conductor like Kubernetes' control plane.

```

1. The decorator onlt does "create span" and says "A pod started."

2. ObserverRunner later says

"Everything is finished.

Close every remaining span.

Emit them.

End trace.

Cleanup."

So ObserverRunner becomes responsible for things like

start_trace()

yield

while there are spans:
    emit(pop_span())

end_trace()
