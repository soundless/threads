/**
 * Created by hengjuntian on 6/6/16.
 */
public class SingleWriterCounter {
    private volatile long count = 0;

    /**
     * Only one thread may ever call this method, or
     * it will lead to race conditions.
     */
    public void inc() {
        this.count++;
    }

    /**
     * Many reading threads may call this method
     * @return
     */
    public long count() {
        return this.count;
    }
}
