import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicStampedReference;

/**
 * Created by hengjuntian on 6/6/16.
 */
public class NonBlockingTemplate {
    public static class IntendedModification {
        public AtomicBoolean completed = new AtomicBoolean(false);
    }

    private AtomicStampedReference<IntendedModification> ongoingModification =
            new AtomicStampedReference<IntendedModification>(null, 0);

    // declare the state of the data stucture here.

    public void modify() {
        while (!attemptModifyASR());
    }

    public boolean attemptModifyASR() {
        boolean modified = false;

        IntendedModification currentlyOngoingModification = ongoingModification.getReference();
        int stamp = ongoingModification.getStamp();

        if (currentlyOngoingModification == null) {
            // copy data structure for use in intended modification

            // prepare intended modification
            IntendedModification newModification = new IntendedModification();

            boolean modificationSubmitted =
                    ongoingModification.compareAndSet(null, newModification, stamp, stamp + 1);

            if (modificationSubmitted) {
                // complete modification via a series of compare-and-swap operations.
                // Note: Other threads may assist in completing the compare-and-swap
                // operation, so some CAS may fail

                modified = true;
            }
        }
        else {
            modified = false;
        }

        return modified;
    }
}
