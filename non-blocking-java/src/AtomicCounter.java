import java.util.concurrent.atomic.AtomicLong;

/**
 * Created by hengjuntian on 6/6/16.
 */
public class AtomicCounter {
    private AtomicLong count = new AtomicLong(0);

    public void inc() {
        boolean updated = false;
        while (!updated) {
            long prevCount = this.cout.get();
            updated = this.count.compareAndSet(prevCount, prevCount + 1);
        }
    }

    public long count() {
        return this.count.get();
    }
}


